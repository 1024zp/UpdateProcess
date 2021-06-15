#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import asyncio
import logging
import requests
from tqdm import tqdm
import aiohttp
from aiohttp import client
from Configure import ConfigProfile
import os


dir_root = os.path.dirname(__file__)
dir_path = os.path.join(dir_root, "release")


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
    def DownLoad(url, name, total_size):
        if not isinstance(url, str):
            raise Exception("url doesn't math str")

        if not isinstance(name, str):
            raise Exception("name doesn't math str")

        requests.packages.urllib3.disable_warnings()
        # r = requests.head(url)
        # if r.status_code not in (200, 206):
        #     r.raise_for_status()
        # else:
        #     pass
        #
        # Content_Length = r.headers.get("Content-Length")
        # if Content_Length is None:
        #     raise Exception("Headers doesn't contain Content-Length.")
        # else:
        #     total_size = int(Content_Length)

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
        return

    """
    @brief  DownLoad function uses as asynchronous
    """

    @staticmethod
    async def ManagerAsynchronous(links, listName):
        await DownLoadPackage.__many(links, listName)

    @staticmethod
    async def __one(session, url, name):
        async with session.get(url) as response:
            file = os.path.join(dir_path, name)
            with open(file, 'wb') as fd:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    fd.write(chunk)
                    fd.flush()

    @staticmethod
    async def __many(links, listName):
        tasks = []  # 保存所有任务的列表
        async with aiohttp.ClientSession() as session:  # aiohttp建议整个应用只创建一个session，不能为每个请求创建一个seesion
            for no, link in enumerate(links, 0):
                file_path = os.path.join(dir_path, listName[no])
                task = asyncio.create_task(DownLoadPackage.__one(session, link, file_path), name=file_path)
                tasks.append(task)
                await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == '__main__':

    lists = []
    names = []
    lists.append("http://52.82.25.201:1080/files/a29e4b92092f840504ab5f77075d7cc2+090cea6c-4862-44b2-9d7a-1c1e39cc19a3")
    names.append("1.deb")
    d = DownLoadPackage()
    for l, n in zip(lists, names):
        d.DownLoad(l, n)

    # loop = asyncio.get_event_loop()
    # fut = asyncio.ensure_future(d.ManagerAsynchronous(lists, names))
    # loop.run_until_complete(fut)
    # print("DownLoad")


    # file = os.path.join(dir_path, "1.deb")
    # ret = os.system('sudo dpkg -i ' + file)
    # if ret != 0:
    #     error = "1.deb install failed."
    #     logging.error(error)
    #     print(error)
    # else:
    #     pass
    # exit(0)



