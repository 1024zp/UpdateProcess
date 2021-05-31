#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


import os
import asyncio
import aiohttp
from Upd.Schedule.SchedulerTask import SchedulerTask
from Upd.Util.Configure import ConfigProfile

basepath = os.path.abspath(os.path.dirname(__file__))


def get_links():
    '''获取所有图片的下载链接'''
    with open(os.path.join(basepath, 'flags.txt')) as f:  # 图片名都保存在这个文件中，每行一个图片名
        return ['http://192.168.40.121/flags/' + flag.strip() for flag in f.readlines()]


async def download_one(session, url, name):
    async with session.get(url) as response:
        image_content = await response.content.read(chunksize=1024)
        if image_content:
            with open(name, 'wb') as f:
                f.write(image_content)


async def download_many():
    links = get_links()
    tasks = []  # 保存所有任务的列表
    async with aiohttp.ClientSession() as session:  # aiohttp建议整个应用只创建一个session，不能为每个请求创建一个seesion
        for no, link in enumerate(links, 1):
            image = {
                'Num': no,  # 图片序号，方便日志输出时，正在下载哪一张
                'link': link
            }
            # asyncio.create_task()是Python 3.7新加的，否则使用asyncio.ensure_future()
            task = asyncio.create_task(download_one(session, image[1], "filename"))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return len(results)


async def print():
    print("Hello World")

def print2():
    print("world")

if __name__ == '__main__':
    sch = SchedulerTask()
    sch.SetConfig(ConfigProfile())
    sch.AddJob(print2(), "print2")
    tasks = asyncio.create_task(print)
    asyncio.run(tasks)
    # count = asyncio.run(download_many())

