#!/usr/bin/env python3
# coding: utf-8
import sys
import sqlite3
from os import path
import os
import re
import time
from datetime import datetime
import ipdb
import traceback
from my_utils import uprint,ulog
from pyquery import PyQuery as pq
from urllib import parse
import html2text
from web_utils import urlChangePath, elmToMd
from postgres_utils import dict2hstore
from collections import OrderedDict
from infix_operator import Infix

def contains_case_ignore(txt:str, pat:str)->bool:
    return pat.lower() in txt.lower()

cicontains=Infix(contains_case_ignore)

conn=None
startTrail=[]
prevTrail=[]

def getStartIdx():
    global startTrail
    if startTrail:
        return startTrail.pop(0)
    else:
        return 0

def sql(query:str, var=None):
    global conn
    csr=conn.cursor()
    try:
        if var:
            rows = csr.execute(query,var)
        else:
            rows = csr.execute(query)
        if not query.startswith('SELECT'):
            conn.commit()
        if query.startswith('SELECT'):
            return rows.fetchall()
        else:
            return
    except sqlite3.Error as ex:
        print(ex)
        raise ex


def fileUrlIsCdn(url)->bool:
    """
    file_url="https://arris--c.na13.content.force.com/sfc/dist/version/downloadNoFlash?oid=00D30000000kUAL&ids=068a00000056x8J&d=%2Fa%2Fa00000001cph%2Fpj2i8MJWmTMCswIVI.Zxv4NnIixJXq9bWs8KpSsNefs"
    not this one http://arris.force.com/consumers/ConsumerProductDetail?p=a0ha000000GNcszAAD&c=DSL%20Modems%20and%20Gateways
    """
    return re.match(r'(http|https)://arris--c.+content\..+', url) is not None

def faqScraper(baseUrl, model, image_url, dev_desc, dev_hstore):
    # http://arris.force.com/consumers/articles/Drivers_and_Firmware/2247-N8-10NA-9-1-1h0d34-Firmware-Upgrade
    global prevTrail
    try:
        ulog('baseUrl= '+baseUrl)
        d = pq(url=baseUrl)
        files = [_ for _ in d('a') if _.text_content()/cicontains/'Firmware']
        numFiles= len(files)
        ulog('numFiles=%s'%numFiles)
        for idx in range(startIdx, numFiles):
            ulog('idx=%s'%idx)
            f=files[idx]
            file_name = f.text_content().strip()
            ulog('file_name="%s"'%file_name)
            try:
                fw_ver = re.search(r"\d+\.([\w\.\-]+)", file_name, re.I).group(0)
            except IndexError:
                ipdb.set_trace()
            file_url = f.attrib['href']
            tree_trail = str(prevTrail+[idx])
            sql("INSERT OR REPLACE INTO TFiles (model, image_url, dev_desc, dev_hstore, fw_ver, page_url, file_url, tree_trail) VALUES (:model, :image_url, :dev_desc, :dev_hstore, :fw_ver, :baseUrl, :file_url, :tree_trail)", locals())
            uprint('UPSERT "%(model)s", "%(fw_ver)s"'%locals())

    except Exception as ex:
        ipdb.set_trace()
        traceback.print_exc()

def detailScraper(baseUrl):
    global prevTrail
    try:
        d = pq(url=baseUrl)
        ulog('baseUrl= '+baseUrl)
        dev_desc = elmToMd(d('div.row')[1])
        model = dev_desc.splitlines()[0].strip()
        assert model
        dev_hstore = [_.text_content().strip() for _ in d('.specTbl tr')]
        dev_hstore = dict2hstore(OrderedDict([(_.splitlines()[0],_.splitlines[1]) for _ in dev_hstore]))

        image_url= d('.box.boxProduct')[0].attrib['style']
        # "background: url(https://arris--c.na13.content.force.com/servlet/servlet.ImageServer?id=015a0000003NYHt&oid=00D30000000kUAL&lastMod=1442430676000);"
        image_url = re.search(r'url\((.+)(?<!\\)\)', image_url).group(1)
        assert fileUrlIsCdn(image_url)

        files = d('#panel4 .small-12.columns:not(.text-center)')
        if not file:
            ulog('No files')
            tree_trail = str(prevTrail)
            sql("INSERT OR REPLACE INTO TFiles (model, image_url, dev_desc, dev_hstore, page_url, tree_trail) VALUES (:model, :image_url, :dev_desc, :dev_hstore, :baseUrl, :tree_trail)", locals())
            uprint('UPSERT "%(models)s"'%model)
            return

        for idx in range(startIdx, len(files)):
            file_name = files[idx].text_content()
            file_name = file_name.splitlines()[0].strip()
            assert file_name
            fw_ver = re.search(r"(\d(\.\d+)*)$", file_name).group(1)
            assert file_name
            file_urls = files[idx].cssselect('a')
            file_url = next(_.attrib['href'] for _ in file_urls if _.text_content().strip().startswith('Download'))
            if not fileUrlIsCdn(file_url):
                faqScraper(file_url, model, image_url, dev_desc, dev_hstore)
            tree_trail = str(prevTrail+[idx])
            sql("INSERT OR REPLACE INTO TFiles (model, image_url, dev_desc, dev_hstore, fw_ver, page_url, file_url, tree_trail) VALUES (:model, :image_url, :dev_desc, :dev_hstore, :fw_ver, :baseUrl, :file_url, :tree_trail)", locals())
            uprint('UPSERT "%(model)s", "%(fw_ver)s"'%locals())
    except Exception as ex:
        ipdb.set_trace()
        traceback.print_exc()

def modelWalker(baseUrl):
    global prevTrail
    try:
        d = pq(url=baseUrl)
        ulog('baseUrl= '+baseUrl)
        models = d('.prodContainer')
        startIdx = getStartIdx()
        numModels = len(models)
        ulog('numModels= %s'%numModels)
        for idx in range(startIdx, numModels):
            model = models[idx]
            onclick = model.attrib['onclick']
            href = re.search(r"'(.+)(?<!\\)'", onclick).group(1)
            prevTrail+=[idx]
            detailWalker(urlChangePath(d.base_url, href))
            prevTrail.pop()
    except Exception as ex:
        ipdb.set_trace()
        traceback.print_exc()

def seriesWalker(baseUrl):
    global prevTrail
    try:
        d = pq(url=baseUrl)
        seriess = d('.prodContainer a.button')
        startIdx = getStartIdx()
        numSeriess = len(seriess)
        ulog('numSeriess=%s'%numSeriess)
        for idx in range(startIdx, numSeriess):
            series = seriess[idx]
            href = series.attrib['href']
            prevTrail+=[idx]
            modelWalker(urlChangePath(d.base_url, href))
            prevTrail.pop()
    except Exception as ex:
        ipdb.set_trace()
        traceback.print_exc()



def main():
    global startTrail,prevTrail, conn
    try:
        startTrail = [int(re.search(r'\d+', _).group(0)) for _ in sys.argv[1:]]
        uprint('startTrail=%s'%startTrail)
        conn=sqlite3.connect('tplink.sqlite3')
        sql(
            "CREATE TABLE IF NOT EXISTS TFiles("
            "id INTEGER NOT NULL,"
            "model TEXT,"
            "image_url TEXT,"
            "dev_desc TEXT,"
            "dev_hstore TEXT,"
            "fw_ver TEXT,"
            "page_url TEXT,"
            "file_url TEXT,"
            "tree_trail TEXT,"
            "file_size INTEGER,"
            "file_sha1 TEXT,"
            "PRIMARY KEY (id)"
            "UNIQUE(model,fw_ver)"
            ");")
        prevTrail=[]
        rootUrl="http://arris.force.com/consumers"
        seriesWalker(rootUrl)
        conn.close()
    except Exception as ex:
        ipdb.set_trace()
        traceback.print_exc()

if __name__=='__main__':
    try:
        main()
    except Exception as ex:
        ipdb.set_trace()
        traceback.print_exc()

