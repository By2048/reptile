# coding=utf-8

import sys
import os
import logging

if sys.platform == "linux":
    keep_path = "/home/am/Pictures/bing"
elif sys.platform == "win32":
    keep_path = "F:\\Image\\Bing"
else:
    logging.error("获取 keep_path 失败 sys.platform = %s" % sys.platform)

temp_path = os.path.join(keep_path, "temp.jpg")


def test_path():
    print(sys.platform)


if __name__ == "__main__":
    test_path()
