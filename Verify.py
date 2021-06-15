#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import hashlib
import os


class Verify:
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

    @staticmethod
    def __read_chunks(fd):
        fd.seek(0)
        chunk = fd.read(128)
        while chunk:
            yield chunk
            chunk = fd.read(128)


dir_root = os.path.dirname(__file__)
dir_path = os.path.join(dir_root, "release")

if __name__ == '__main__':
    v = Verify()
    file = os.path.join(dir_path, "1.deb")
    md5 = v.MakeMD5(file)
    if md5 == "f377ac9ad1313b8eb2f6b997811b1c7a":
        print(md5)
