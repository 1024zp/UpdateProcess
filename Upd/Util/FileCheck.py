#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import hashlib
import os


class FileCheck:

    __md5 = None

    def __init__(self):
        pass

    def MakeMD5(self, fname):
        m = hashlib.md5()
        if isinstance(fname, str) and os.path.exists(fname):
            with open(fname, "rb") as f:
                for chunk in self.__read_chunks(f):
                    m.update(chunk)
        return m.hexdigest()

    def CompareMD5(self, fname, md5):
        if isinstance(fname, str) and os.path.exists(fname):
            with open(fname, "r") as f:
                size = os.path.getsize(fname)
                self.__md5 = f.read(size)
        if self.__md5 == md5:
            return True
        else:
            return False

    @staticmethod
    def __read_chunks(fd):
        fd.seek(0)
        chunk = fd.read(128)
        while chunk:
            yield chunk
            chunk = fd.read(128)


if __name__ == '__main__':
    sstr = "i love hanyu"
    md5 = hashlib.md5(sstr.encode(encoding='utf-8')).hexdigest()
    print(md5)

    with open("readme", "w") as f:
        f.write(sstr)

    with open("readme.md5", "w") as f:
        f.write(md5)

    check = FileCheck()
    genhex = check.MakeMD5("readme")
    rv = check.CompareMD5("readme.md5", genhex)
    if rv:
        print("equal")
    else:
        print("differ")
