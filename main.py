#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import json
import logging
import os
import shutil
from apscheduler.schedulers.blocking import BlockingScheduler
from Configure import ConfigProfile
from DownLoad import DownLoadPackage
from Query import QueryClient
from Verify import Verify
import tkinter as tk
from tkinter import messagebox

import logging

logger = logging.getLogger("logging")
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("logging.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class Update_Soft:

    def __init__(self):
        self.__lists_uri = {}
        self.__lists_md5 = {}
        self.__size = {}
        self.__backup = {}
        self.__config = ConfigProfile()
        self.__config.GetInstance()
        self.__dirPath = os.path.join(self.__config[self.__config.PATH], "UpdPackage")
        self.__filePath = os.path.join(self.__dirPath, "version_control.record")
        if not os.path.exists(self.__dirPath):
            os.mkdir(self.__dirPath)
        logger = os.path.join(self.__dirPath, "logging.log")
        if not os.path.exists(logger):
            with open(logger, "w") as f:
                pass
        logging.basicConfig(filename=logger, filemode="w", level=logging.ERROR,
                            format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s')

    def Query(self):
        q = QueryClient()
        if not os.path.exists(self.__filePath):
            with open(self.__filePath, "w") as f:
                pass
        query_json = json.loads(q.Query())
        record_json = []
        s = q.Load_record(self.__filePath)
        if len(s) != 0:
            record_json = json.loads(s)
        length = self.GetItem(q, record_json, query_json)
        if length != 0:
            with open(self.__filePath, "w") as f:
                json.dump(json.loads(q.Query()), f, ensure_ascii=False, indent=4)
        print("Query")

    def GetItem(self, q, record_json, query):
        for y in record_json:
            for x in query:
                if y[q.FILE_NAME] == x[q.FILE_NAME] and x[q.VERSION_NAME] == y[q.VERSION_NAME]:
                    query.remove(x)
        for index in query:
            name = index[q.FILE_NAME]
            self.__lists_uri[name] = index[q.FILE_PATH]
            self.__lists_md5[name] = index[q.FILE_HASH]
            self.__size[name] = index[q.FILE_SIZE]
            self.__backup[name] = name
        return len(query)

    def DownLoad(self):
        if len(self.__lists_uri) == 0 or len(self.__size) == 0:
            return
        d = DownLoadPackage()
        for n in self.__lists_uri:
            file = os.path.join(self.__dirPath, n)
            d.DownLoad(self.__lists_uri[n], file, int(self.__size[n]))
        print("DownLoad")

    def Verify(self):
        if len(self.__lists_md5) == 0:
            return
        v = Verify()
        for name in self.__lists_md5:
            fname = os.path.join(self.__dirPath, name)
            md5 = v.MakeMD5(fname)
            if md5 != self.__lists_md5[name]:
                self.__lists_uri.pop(name)
                os.remove(fname)
                self.__backup.pop(name)
                error = name + " verify failed."
                logging.error(error)
        print("Verify")

    def Update(self):
        if len(self.__lists_uri) == 0:
            return
        for name in self.__lists_uri:
            file = os.path.join(self.__dirPath, name)
            ret = os.system('sudo dpkg -i ' + file)
            if ret != 0:
                error = name + " install failed."
                logging.error(error)
            else:
                print("success", name)
        print("Update")

    def Start(self):
        interval = self.__config[self.__config.Interval]
        hours = int(interval[self.__config.Hours])
        minutes = int(interval[self.__config.Minutes])
        seconds = int(interval[self.__config.Seconds])
        scheduler = BlockingScheduler()
        scheduler.add_job(func=self.Run, trigger='interval', hours=hours, minutes=minutes,
                          seconds=seconds, id="Update_Soft")

        scheduler.start()

    def BackUp(self):
        path = os.path.join(self.__dirPath, "bak")
        if not os.path.exists(path):
            os.mkdir(path)
        if len(self.__backup) == 0:
            return
        for i in self.__backup:
            file = os.path.join(self.__dirPath, i)
            shutil.copy(file, path)

    def Remove(self):
        for i in self.__backup:
            file = os.path.join(self.__dirPath, i)
            os.remove(file)

    def Message(self):
        if len(self.__lists_uri) == 0:
            return
        string = "[ "
        for name in self.__lists_uri:
            string += name
            string += "   "
        string += " ]"
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(title="更新成功软件包列表", message=string)
        root.destroy()

    def Clean(self):
        self.__backup.clear()
        self.__size.clear()
        self.__lists_uri.clear()
        self.__lists_md5.clear()

    def Run(self):
        try:
            self.Query()
            self.DownLoad()
            self.Verify()
            # self.Update()
            self.BackUp()
            self.Remove()
            self.Message()
            self.Clean()
        except Exception as e:
            self.Clean()
            logging.error(e)





if __name__ == '__main__':
    u = Update_Soft()
    u.Start()
