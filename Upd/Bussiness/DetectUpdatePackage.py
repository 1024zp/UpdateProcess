#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


import requests
import json


class DetectUpdatePackage:

    def __init__(self):
        pass

    @staticmethod
    def DetectUpd(url):
        dicts = ["https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fyouimg1.c-ctrip.com%2Ftarget%2Ftg%2F035"
                 "%2F063%2F726%2F3ea4031f045945e1843ae5156749d64c.jpg&refer=http%3A%2F%2Fyouimg1.c-ctrip.com&app"
                 "=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1624776917&t=a11fadae30e5a4091949919e14fec4b6",
                 "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fwx1.sinaimg.cn%2Flarge"
                 "%2F008fHVgdly4gqfhftvhl5j30u00iv40g.jpg&refer=http%3A%2F%2Fwx1.sinaimg.cn&app=2002&size=f9999,"
                 "10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1624777075&t=e383955b1fcaf1c7ad85932df88eb42c"]
        return 0, dicts


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
