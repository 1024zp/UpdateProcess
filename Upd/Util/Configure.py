#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import json
import logging
import threading


class ConfigProfile:
    """
    this file use to Configuration profile
    support internal function __setitem__ and __getitem__
    you can use it to set dict by <class>[key]=value or get value from <class>[key]

    @brief
    Enum field use to be static const values,do not attempt to change it.

    Public Function:

        @brief "read content from json file,and deserialize to string"
        @param [filename]
        ReadFromJsonFile(self, filename)

        @brief "write content that json string  to file"
        @param [filename]
        WriteToJsonFile(self, filename)
    """

    """
    @brief this field use to named download file.
    """

    """
    @brief this field use to set config items.
    """
    ServerDomain = "ServerDomain"
    ServerPort = "ServerPort"
    TimeOut = "TimeOut"
    Interval = "Interval"
    Hours = "Hours"
    Minutes = "Minutes"
    Seconds = "Seconds"
    URI_Auth = "URI_Auth"
    URI_Detect = "URI_Detect"
    URI_DownLoad = "URI_DownLoad"
    URI_RollBack = "URI_RollBack"
    Config_File = "Config_File"
    SchedulerLog = "SchedulerLog"

    SCHEDULER_NAME = "SchedulerLog.log"
    CONFIG_NAME = "Config.json"
    __mutex = threading.Lock()
    __instance = None
    __dict = {}

    def __init__(self):

        self.__dict = {self.ServerDomain: None, self.ServerPort: None, self.TimeOut: None, self.Interval: None,
                       self.URI_Auth: None, self.URI_Detect: None, self.URI_DownLoad: None, self.URI_RollBack: None,
                       self.Config_File: self.CONFIG_NAME, self.SchedulerLog: self.SCHEDULER_NAME}

    def __new__(cls, *args, **kwargs):
        with ConfigProfile.__mutex:
            if not cls.__instance:
                cls.__instance = object.__new__(cls)
        return cls.__instance

    """
    If the current class contains the attribute, set its variable value
    """

    def __setitem__(self, key, value):
        if isinstance(key, str):
            if not self.__dict.__contains__(key):
                raise Exception("the dict doesn't contain the key named %s" % key)
            if isinstance(value, (dict, int, str, list)):
                self.__dict[key] = value
            else:
                raise Exception(logging.WARNING, "value's type is not in support list (int, str, dict)")
        else:
            raise Exception("""the %s doesn't have the attribute %s or the %s is not in support list (str)"""
                            % (self.__class__, key, key))
        return 0

    """
    search the key if the current class contains the attribute,return the value
    """
    def __getitem__(self, item):
        if hasattr(self, item):
            return self.__dict[item]
        else:
            return -1, "get item from dict failed,doesn't contain %s" % item

    def GetInstance(self):
        rv, err = self._readFromJsonFile(self.__dict[self.Config_File])
        if rv != 0:
            return rv, err
        else:
            return rv, self.__dict

    """
    read content from json file,and deserialize to string
    """

    def _readFromJsonFile(self, filename):
        if isinstance(filename, str) and len(filename) != 0:
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    self.__dict = json.load(f)
                    return 0, self.__dict
            else:
                return -1, "the file doesn't exits"
        else:
            return -1, "the file name is ont support in list (str) or it's none"

    """
    write content that json string  to file 
    """

    def writeToJsonFile(self, filename):
        if len(self.__dict) == 0:
            return -1, "not set %s dict" % self.__class__
        if isinstance(filename, str) and len(filename) != 0:
            with open(filename, "w") as f:
                return json.dump(self.__dict, f, indent=4, separators=(",", ":")), None
        else:
            return -1, "the file name is ont support in list (str) or it's none"


if __name__ == '__main__':
    const = ConfigProfile()
    const[const.ServerDomain] = "None"
    const[const.ServerPort] = 8080
    const[const.TimeOut] = 30
    const[const.Interval] = {const.Hours: 1, const.Minutes: 2, const.Seconds: 3}

    const[const.URI_Auth] = "https://www.Auth.com"
    const[const.URI_Detect] = "https://www.Detect.com"
    const[const.URI_DownLoad] = "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fattach.bbs.miui.com%2Fforum%2F201409" \
                            "%2F09%2F130415ome6e930vp99to05.jpg&refer=http%3A%2F%2Fattach.bbs.miui.com&app=2002&size" \
                            "=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1624501298&t=925e21a2d9d98dac6831e4efcc7f2500 "
    const[const.URI_RollBack] = "https://www.RollBack.com"
    const[const.SchedulerLog] = const.SCHEDULER_NAME
    const.writeToJsonFile(const[const.Config_File])
