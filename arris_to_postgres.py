#!/usr/bin/env python3
# coding:utf-8
import sqlite3
import psycopg2
from psycopg2 import errorcodes
import sys
from my_utils import uprint
from GridIotCredentials import GridIotConnStr
import ipdb
import traceback

ouconn=None
def ousql(query,var=None):
    global ouconn
    oucsr=ouconn.cursor()
    try:
        oucsr.execute(query,var)
        if not query.startswith('SELECT'):
            ouconn.commit()
        if query.startswith('SELECT') or 'RETURNING' in query:
            return oucsr.fetchall()
        else:
            return
    except psycopg2.Error as ex:
        oucsr.execute('ABORT')
        raise ex

def main():
    brand='Arris'
    source='arris.force.com/consumers'
    rev=""
    startInRowIdx=int(sys.argv[1]) if len(sys.argv)>1 else 0
    
    with sqlite3.connect('arris.sqlite3') as inconn:
        incsr = inconn.cursor()
        global ouconn
        ouconn= psycopg2.connect(GridIotConnStr)
        inRows = incsr.execute(
            "SELECT model, image_url, dev_desc, dev_hstore, fw_ver, page_url"
            ", file_url, file_size, file_sha1 "
            " FROM TFiles "
            " ORDER BY id LIMIT -1 OFFSET %d"%startInRowIdx)
        for inRowIdx, inRow in enumerate(inRows,startInRowIdx):
            model,image_url,dev_desc,dev_hstore,fwVer,page_url,file_url,file_size,file_sha1=inRow
            uprint('inRowIdx=%s, model="%s","%s" '%(
                inRowIdx, model,fwVer))

            # UPSERT new Device
            devId=ousql(
                "UPDATE TDevice SET source=%(source)s,"
                " image_url=%(image_url)s, "
                " description=%(dev_desc)s, "
                " support_page=%(page_url)s, "
                " speedguide_props_hstore=%(dev_hstore)s::hstore "
                "WHERE brand=%(brand)s AND model=%(model)s AND"
                " revision=%(rev)s RETURNING id" ,locals())
            if devId:
                devId=devId[0][0]
            else:
                devId=ousql(
                    "INSERT INTO TDevice (brand,model,revision,source,"
                    "image_url,description,support_page,speedguide_props_hstore"
                    ")VALUES(%(brand)s,%(model)s,%(rev)s,%(source)s,%(image_url)s"
                    ",%(dev_desc)s,%(page_url)s,%(dev_hstore)s::hstore)"
                    " RETURNING id",
                    locals())
                devId=devId[0][0]
            uprint("UPSERT brand='%(brand)s', model=%(model)s"
                ",source=%(source)s RETURNING devId=%(devId)s"%locals())

            # UPSERT new Firmware
            if not fwVer:
                continue
            fwId=ousql(
                "UPDATE TFirmware SET file_sha1=%(file_sha1)s,"
                " include_prev=false,file_size=%(file_size)s,"
                " file_url=%(file_url)s,"
                " desc_url=%(page_url)s "
                "WHERE"
                "  device_id=%(devId)s AND version=%(fwVer)s AND"
                "  exclude_self=false RETURNING id",locals())
            if fwId:
                fwId=fwId[0][0]
            else:
                fwId=ousql(
                    "INSERT INTO TFirmware("
                    "  device_id, version, exclude_self, "
                    "  file_sha1, file_size, "
                    "  file_url, desc_url ) "
                    "VALUES ( %(devId)s, %(fwVer)s, false, "
                    " %(file_sha1)s, %(file_size)s, "
                    " %(file_url)s, %(page_url)s)"
                    " RETURNING id", locals())
                fwId=fwId[0][0]
            uprint("UPSERT TFirmware devId='%(devId)d', fwVer='%(fwVer)s',"
                " sha1='%(file_sha1)s', fwId=%(fwId)d"%locals())

if __name__=='__main__':
    main()
