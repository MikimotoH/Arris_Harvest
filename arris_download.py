#!/usr/bin/env python3
# coding: utf-8
import sqlite3
import ipdb
import traceback
import sys
from ftp_credentials import ftpHostName,ftpUserName,ftpPassword
import ftputil
from os import path
from urllib import parse
import os
from my_utils import uprint
from web_utils import getFileSha1
from web_utils import downloadFile
from datetime import datetime
import re
import urllib

conn=None
        

def main():
    global startTrail,prevTrail,conn
    try:
        startIdx = int(sys.argv[1]) if len(sys.argv)>1 else 0
        conn= sqlite3.connect('arris.sqlite3')
        csr=conn.cursor()
        rows = csr.execute(
            "SELECT id,file_url,file_sha1 FROM TFiles ORDER BY id "
            "LIMIT -1 OFFSET %d"%startIdx
            ).fetchall()
        for idx, row in enumerate(rows,startIdx):
            devId,file_url,file_sha1 = row
            if not file_url:
                continue
            if file_sha1:
                continue
            uprint('idx=%d'%idx)
            local_file  = downloadFile(file_url, "Content-Disposition")
            file_sha1 = getFileSha1(local_file)
            file_size = path.getsize(local_file)
            csr.execute(
                "UPDATE TFiles SET file_sha1=:file_sha1,file_size=:file_size"
                " WHERE id = :devId", locals())
            conn.commit()
            ftp = ftputil.FTPHost(ftpHostName,ftpUserName,ftpPassword)
            uprint('upload to GRID')
            ftp.upload(local_file, path.basename(dstPath))
            ftp.close()
            os.remove(local_file)
    except Exception as ex:
        ipdb.set_trace()
        traceback.print_exc()

if __name__=='__main__':
    main()
