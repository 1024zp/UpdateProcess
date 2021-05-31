#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import time

import requests
from tqdm import tqdm
from apscheduler.events import EVENT_JOB_EXECUTED


class DownLoadPackage():
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

    @staticmethod
    def DownLoad(url, name):

        if not isinstance(url, str):
            raise Exception("url doesn't math str")

        if not isinstance(name, str):
            raise Exception("url doesn't math str")

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

        headers = {'Range': 'bytes=%d-' % temp_size}
        res = requests.get(url, headers=headers, stream=True, verify=False)
        if res.status_code in (200, 206):
            with(open(name, "ab")) as f:
                with tqdm(total=total_size, initial=temp_size, colour='green', desc="下载进度") as t:
                    for chunk in res.iter_content(chunk_size=1024):
                        t.update(len(chunk))
                        f.write(chunk)
                        f.flush()
                        time.sleep(0.01)
        else:
            res.raise_for_status()
        return {"first": "Hello", "second": "World"}


if __name__ == '__main__':

    download = DownLoadPackage()
    download.SetURL("https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fyouimg1.c-ctrip.com%2Ftarget%2Ftg%2F035"
                    "%2F063%2F726%2F3ea4031f045945e1843ae5156749d64c.jpg&refer=http%3A%2F%2Fyouimg1.c-ctrip.com&app"
                    "=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1624776917&t=a11fadae30e5a4091949919e14fec4b6")
    download.SetFileName("jpg")
    download.run()
    download.start()
    download.join()
    exp = download.GetException()
    if exp is not None:
        print(exp)
