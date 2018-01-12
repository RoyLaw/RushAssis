#!/usr/bin/env python

# encoding: utf-8

'''

@author: Roy Law

@license: (C) Copyright 2018.

@contact: roy.law@qq.com

@file: rush_assistant.py

@time: 2018/1/13 上午1:20

@desc:

'''

import time
from common import quiz_json_fetcher

def main():
    while True:
        print(time.strftime('%H:%M:%S',time.localtime(time.time())))
        print(quiz_json_fetcher.get_answer())
        time.sleep(1)


if __name__ == '__main__':
    main()