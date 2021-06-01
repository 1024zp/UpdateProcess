#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import asyncio


class CoroutineTask:

    def __init__(self):
        self.__lists = []
        self.__result = []
        self.__loop = asyncio.get_event_loop()

    def CreateCoroutine(self, cor, task_id):
        task = self.__loop.create_task(cor, name=task_id)
        self.__lists.append(task)

    def StartCoroutine(self):
        fut = asyncio.ensure_future(self.__main())
        self.__loop.run_until_complete(fut)
        try:
            pass
            # self.__loop.run_forever()
        except (KeyboardInterrupt, Exception):
            self.__loop.stop()

    async def __main(self):
        self.__result = await asyncio.gather(*self.__lists, return_exceptions=True)
        print(self.__result)

    def GetResult(self):
        return self.__result


if __name__ == '__main__':
    from UpdateProcess.Upd.Bussiness.DownLoadPackage import DownLoadPackage
    c = CoroutineTask()
    name = "name_"
    j = 0
    lists = ["https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fyouimg1.c-ctrip.com%2Ftarget%2Ftg%2F106%2F069"
             "%2F371%2F3f53bff8412e46deb6e59af671bb1529.jpg&refer=http%3A%2F%2Fyouimg1.c-ctrip.com&app=2002&size"
             "=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1625040988&t=d3cb3f4c061ad66e7858b8a97808080e",
             "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fcar0.autoimg.cn%2Fupload%2Fspec%2F4945"
             "%2Fu_20120220072722314264.jpg&refer=http%3A%2F%2Fcar0.autoimg.cn&app=2002&size=f9999,"
             "10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1625043930&t=c6d5ceb16ecc7e6f0ba985c9dd9fd3d9",
             "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fwx1.sinaimg.cn%2Flarge"
             "%2F008fHVgdly4gqfhftvhl5j30u00iv40g.jpg&refer=http%3A%2F%2Fwx1.sinaimg.cn&app=2002&size=f9999,"
             "10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1625043930&t=59fae86d249faf6382e8fd7e0845b84b"]
    for i in lists:
        coroutine = DownLoadPackage().DownLoad(i, name + str(j))
        c.CreateCoroutine(coroutine, name)
        j += 1
    c.StartCoroutine()
