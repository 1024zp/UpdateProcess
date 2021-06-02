#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import asyncio
import os
import requests
from tqdm import tqdm
import aiohttp
from aiohttp import client


class DownLoadPackage:
    """
    this file use to download update package from remote server domain

    DownLoad(url,name)
    @brief
    This function uses to download file form url which parameter supported.
    Your should also support a file name which uses to write bytes from web
    page.
    @return [rv,err]
    rv  return error code typed by int
    err return typical error info.
    """

    def __init__(self):
        pass

    """
    @brief  DownLoad function uses as synchronization 
    """

    @staticmethod
    def DownLoad(url, name):
        if not isinstance(url, str):
            raise Exception("url doesn't math str")

        if not isinstance(name, str):
            raise Exception("name doesn't math str")

        requests.packages.urllib3.disable_warnings()
        r = requests.head(url)
        if r.status_code not in (200, 206):
            r.raise_for_status()
        else:
            pass

        Content_Length = r.headers.get("Content-Length")
        if Content_Length is None:
            raise Exception("Headers doesn't contain Content-Length.")
        else:
            total_size = int(Content_Length)

        if not os.path.exists(name):
            with open(name, "ab") as f:
                pass
        else:
            pass

        temp_size = os.path.getsize(name)
        if temp_size == total_size:
            with open(name, "w") as f:
                f.seek(0)
                f.truncate()
                temp_size = 0

        headers = {'Range': 'bytes=%d-' % temp_size}
        res = requests.get(url, headers=headers, stream=True, verify=False)
        if res.status_code in (200, 206):
            with(open(name, "ab")) as f:
                with tqdm(total=total_size, initial=temp_size, colour='green', desc="下载进度") as t:
                    for chunk in res.iter_content(chunk_size=1024):
                        t.update(len(chunk))
                        f.write(chunk)
                        f.flush()
        else:
            res.raise_for_status()
        return 0

    """
    @brief  DownLoad function uses as asynchronous
    """
    @staticmethod
    async def ManagerAsynchronous(links):
        await DownLoadPackage.__many(links)

    @staticmethod
    async def __one(session, url, name):
        async with session.get(url) as response:
            with open(name, 'wb') as fd:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    fd.write(chunk)
                    fd.flush()
        return 0

    @staticmethod
    async def __many(links):
        tasks = []  # 保存所有任务的列表
        async with aiohttp.ClientSession() as session:  # aiohttp建议整个应用只创建一个session，不能为每个请求创建一个seesion
            for no, link in enumerate(links, 1):
                file = "name_" + str(no)
                task = asyncio.create_task(DownLoadPackage.__one(session, link, file), name=file)
                tasks.append(task)
            result = await asyncio.gather(*tasks, return_exceptions=True)
            for i in result:
                print(i)




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


if __name__ == '__main__':
    d = DownLoadPackage()
    loop = client.get_running_loop()
    fut = asyncio.ensure_future(d.ManagerAsynchronous(get_links()))
    loop.run_until_complete(fut)

    # download = DownLoadPackage()
    # download.SetURL("https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fyouimg1.c-ctrip.com%2Ftarget%2Ftg%2F035"
    #                 "%2F063%2F726%2F3ea4031f045945e1843ae5156749d64c.jpg&refer=http%3A%2F%2Fyouimg1.c-ctrip.com&app"
    #                 "=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1624776917&t=a11fadae30e5a4091949919e14fec4b6")
    # download.SetFileName("jpg")
    # download.run()
    # download.start()
    # download.join()
    # exp = download.GetException()
    # if exp is not None:
    #     print(exp)
