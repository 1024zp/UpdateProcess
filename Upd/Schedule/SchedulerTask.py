#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BlockingScheduler
import logging
from Upd.Util.Configure import ConfigProfile
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from Upd.Bussiness.DownLoadPackage import DownLoadPackage


class SchedulerTask:
    __configure = None

    def __init__(self):
        self.__scheduler = BlockingScheduler()
        self.__scheduler._logger = logging
        self.__dicts = {}

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

    def PauseJob(self):
        self.__scheduler.pause()

    def Wakeup(self):
        self.__scheduler.wakeup()

    def Start(self):
        self.__scheduler.start()

    def say_hello(self):
        with tqdm(total=100, initial=0, colour='green', desc="进度") as t:
            for i in range(100):
                t.update(1)
                time.sleep(0.01)
        print("exits")
        self.__scheduler.resume()
        return 0


    def Listener(self, Event):
        print("id : ", Event.retval)
        job = self.__scheduler.get_job(Event.job_id)
        if Event.code == EVENT_JOB_EXECUTED:
            print('任务照常运行！！！！！！')
            self.__scheduler.pause()
            self.say_hello()
        else:
            pass

    def AddListener(self):
        self.__scheduler.add_listener(self.Listener, mask=EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)


# async def main():
#     task = SchedulerTask()
#     task.SetConfig(ConfigProfile())
#     task.AddJob(print2, "print2")
#     task.Start()
#     task1 = asyncio.create_task(
#     task2 = asyncio.create_task(
#     asyncio.gather(task1, task2)
#     await task1
#     await task2
#     print("result : ", task1.result())
#     for i in task.GetJobs():
#         print(i.name)

from tqdm import tqdm


def main():
    task = SchedulerTask()
    task.SetConfig(ConfigProfile())
    task.AddJob(function=DownLoadPackage().DownLoad, job_id="DownLoad", args=(
        "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fwx2.sinaimg.cn%2Flarge%2F008fHVgdly4gqfhfts4vrj30u00ji75u.jpg&refer=http%3A%2F%2Fwx2.sinaimg.cn&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1625019989&t=7b0be857ec9a337fa8f6b40069fd025e",
        "files"))
    task.AddListener()
    task.Start()


    # res = task.get_jobs()
    # print(res)
    # task1 = asyncio.create_task(say_Hi())
    # asyncio.gather(task1)
    # await task1
    # await asyncio.sleep(1)


if __name__ == '__main__':
    main()

    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop.run_until_complete(main())
    # asyncio.run(say_Hi())
