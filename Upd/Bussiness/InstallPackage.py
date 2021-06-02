#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import asyncio
import aiohttp
from aiohttp import client


def get_links():
    lists = ["https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fyouimg1.c-ctrip.com%2Ftarget%2Ftg%2F106%2F069"
             "%2F371%2F3f53bff8412e46deb6e59af671bb1529.jpg&refer=http%3A%2F%2Fyouimg1.c-ctrip.com&app=2002&size"
             "=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1625040988&t=d3cb3f4c061ad66e7858b8a97808080e",
             "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fcar0.autoimg.cn%2Fupload%2Fspec%2F4945"
             "%2Fu_20120220072722314264.jpg&refer=http%3A%2F%2Fcar0.autoimg.cn&app=2002&size=f9999,"
             "10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1625043930&t=c6d5ceb16ecc7e6f0ba985c9dd9fd3d9",
             "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fwx1.sinaimg.cn%2Flarge"
             "%2F008fHVgdly4gqfhftvhl5j30u00iv40g.jpg&refer=http%3A%2F%2Fwx1.sinaimg.cn&app=2002&size=f9999,"
             "10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1625043930&t=59fae86d249faf6382e8fd7e0845b84b"]
    return lists

    # '''获取所有图片的下载链接'''
    # with open(os.path.join(basepath, 'flags.txt')) as f:  # 图片名都保存在这个文件中，每行一个图片名
    #     return ['http://192.168.40.121/flags/' + flag.strip() for flag in f.readlines()]


async def download_one(session, url, name):
    if name == "name_2":
        raise Exception("Hello")
    async with session.get(url) as response:
        with open(name, 'wb') as fd:
            while True:
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                fd.write(chunk)
                fd.flush()
    return 0


async def download_many():
    links = get_links()
    tasks = []  # 保存所有任务的列表
    async with aiohttp.ClientSession() as session:  # aiohttp建议整个应用只创建一个session，不能为每个请求创建一个seesion
        for no, link in enumerate(links, 1):
            file = "name_" + str(no)
            task = asyncio.create_task(download_one(session, link, file), name=file)
            tasks.append(task)
        result = await asyncio.gather(*tasks, return_exceptions=True)
        for i in result:
            print(i)


async def main(lists):
    await download_many()

if __name__ == '__main__':
    loop = client.get_running_loop()
    fut = asyncio.ensure_future(main(get_links()))
    loop.run_until_complete(fut)

    try:
        loop.run_forever()
    except Exception as e:
        loop.stop()
