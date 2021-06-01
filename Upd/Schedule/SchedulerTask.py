#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from threading import Event


class SchedulerTask:
    """
    SchedulerTask uses to manager job,through below which wrap up.

    AddJob(self, function, job_id, args=None)
        @brief
            function *func
            job_id
            args      f's parameter
    SetConfig(self, config)
        @brief config is a ConfigProfile instance

    Start_job(self)
    Pause_job(self, job_id)
    Resume_job(self, job_id)
    AddListener(self)

    Listener(self, Event)

    GetResult(self)
    ClearResult(self)
    """

    def __init__(self):
        self.__scheduler = BlockingScheduler()
        self.__scheduler._logger = logging
        self.__configure = None
        self.__events = Event()
        self.__events.clear()
        self.__lists = []

    def SetConfig(self, config):
        self.__configure = config
        try:
            rv, err = self.__configure.GetInstance()
        except Exception as e:
            logging.warning(e)
        else:
            if rv != 0:
                return -1, err
            else:
                logging.basicConfig(filename=self.__configure[self.__configure.SchedulerLog], level=logging.ERROR)
                return 0, None

    def AddJob(self, function, job_id, args=None):
        interval = self.__configure[self.__configure.Interval]
        hours = int(interval[self.__configure.Hours])
        minutes = int(interval[self.__configure.Minutes])
        seconds = int(interval[self.__configure.Seconds])
        self.__scheduler.add_job(func=function, trigger='interval', hours=hours, minutes=minutes,
                                 seconds=seconds, id=job_id, args=args)

    def Start_job(self):
        self.__scheduler.start()

    def Pause_job(self, job_id):
        self.__scheduler.pause_job(job_id=job_id)

    def Resume_job(self, job_id):
        self.__scheduler.resume_job(job_id=job_id)

    def AddListener(self):
        self.__scheduler.add_listener(self.Listener, mask=EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    def Listener(self, Event):
        if Event.code == EVENT_JOB_EXECUTED:
            if Event.retval is not None:
                self.__lists = Event.retval
                print(self.__lists)
                self.Pause_job(Event.job_id)
        else:
            logging.warning(Event.exception)

    def GetResult(self):
        return self.__lists

    def ClearResult(self):
        self.__lists.clear()


from UpdateProcess.Upd.Bussiness.DownLoadPackage import DownLoadPackage
from UpdateProcess.Upd.Util.Configure import ConfigProfile

if __name__ == '__main__':
    lists = ["https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fyouimg1.c-ctrip.com%2Ftarget%2Ftg%2F106%2F069"
             "%2F371%2F3f53bff8412e46deb6e59af671bb1529.jpg&refer=http%3A%2F%2Fyouimg1.c-ctrip.com&app=2002&size"
             "=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1625040988&t=d3cb3f4c061ad66e7858b8a97808080e",
             "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fcar0.autoimg.cn%2Fupload%2Fspec%2F4945"
             "%2Fu_20120220072722314264.jpg&refer=http%3A%2F%2Fcar0.autoimg.cn&app=2002&size=f9999,"
             "10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1625043930&t=c6d5ceb16ecc7e6f0ba985c9dd9fd3d9",
             "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fwx1.sinaimg.cn%2Flarge"
             "%2F008fHVgdly4gqfhftvhl5j30u00iv40g.jpg&refer=http%3A%2F%2Fwx1.sinaimg.cn&app=2002&size=f9999,"
             "10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1625043930&t=59fae86d249faf6382e8fd7e0845b84b"]

    s = SchedulerTask()
    s.SetConfig(ConfigProfile())
    s.AddListener()
    d = DownLoadPackage()
    num = 0
    for i in lists:
        file = "name_" + str(num)
        s.AddJob(function=d.DownLoad, job_id=file, args=[i, file])
        num += 1
    s.Start_job()
