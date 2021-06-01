#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import time

import requests
import json


class DetectUpdatePackage:

    def __init__(self):
        pass

    async def DetectUpd(self, url=None):
        lists = ["https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fyouimg1.c-ctrip.com%2Ftarget%2Ftg%2F106%2F069"
                 "%2F371%2F3f53bff8412e46deb6e59af671bb1529.jpg&refer=http%3A%2F%2Fyouimg1.c-ctrip.com&app=2002&size"
                 "=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1625040988&t=d3cb3f4c061ad66e7858b8a97808080e",
                 "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fcar0.autoimg.cn%2Fupload%2Fspec%2F4945"
                 "%2Fu_20120220072722314264.jpg&refer=http%3A%2F%2Fcar0.autoimg.cn&app=2002&size=f9999,"
                 "10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1625043930&t=c6d5ceb16ecc7e6f0ba985c9dd9fd3d9",
                 "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fwx1.sinaimg.cn%2Flarge"
                 "%2F008fHVgdly4gqfhftvhl5j30u00iv40g.jpg&refer=http%3A%2F%2Fwx1.sinaimg.cn&app=2002&size=f9999,"
                 "10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1625043930&t=59fae86d249faf6382e8fd7e0845b84b"]

        print("DetectUpd -- ", time.time())
        return lists


if __name__ == '__main__':
    download = DetectUpdatePackage()
    rv, err = download.DetectUpd("https://gimg2.baidu.com/image_search/src"
                                 "=Bussiness%3A%2F%2Fattach.bbs.miui.com%2Fforum%2F201603%2F28"
                                 "%2F211033ywhstjcmzjhhzihw. "
                                 "jpg&refer=Bussiness%3A%2F%2Fattach.bbs.miui.com&app=2002&size=f9999,"
                                 "10000&q=a80&n=0&g= "
                                 "0n&fmt=jpeg?sec=1624179961&t=2cd1f5d5788f55449f6041acb871dc53")
    print(err)
    print(rv)
