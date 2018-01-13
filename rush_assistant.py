#!/usr/bin/env python

# encoding: utf-8

'''

@author: Roy Law

@license: (C) Copyright 2018.

@contact: https://github.com/RoyLaw

@file: rush_assistant.py

@time: 2018/1/13 上午1:20

@desc:

'''


import time
from common import quiz_json_fetcher, answer_searcher


def main():
    while True:
        # print(time.strftime('%H:%M:%S', time.localtime(time.time())))
        question, options = quiz_json_fetcher.get_quiz()
        answer_searcher.search_quiz(question, options)
        time.sleep(1)


if __name__ == '__main__':
    main()
