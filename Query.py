#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import logging
import requests
from Configure import ConfigProfile
import json
import os
from DownLoad import DownLoadPackage
from Verify import Verify
import asyncio


loger = logging.getLogger("logging.sub")

class QueryClient:
    CREATE_AT = "create_at"
    FILE_HASH = "file_hash"
    FILE_NAME = "file_name"
    FILE_PATH = "file_path"
    FILE_SIZE = "file_size"
    ITER_NAME = "item_name"
    VERSION_INFO = "version_info"
    VERSION_NAME = "version_name"

    def __init__(self):
        self.__config = ConfigProfile()
        self.__config.GetInstance()
        self.__url = self.__config[self.__config.URI_Detect]

    def Query(self):
        requests.packages.urllib3.disable_warnings()
        res = requests.get(self.__url, timeout=5, verify=False)
        if res.status_code in (200, 206):
            return json.dumps(res.json(), sort_keys=True, indent=4, separators=(',', ': '))
        else:
            loger.error("WFKSIFJSEOFJESOFJSOFOJ")
            res.raise_for_status()


    @staticmethod
    def Load_record(record_file):
        with open(record_file, "r") as f:
            return f.read()


if __name__ == '__main__':
    pass
