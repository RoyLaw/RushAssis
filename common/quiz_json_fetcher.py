#!/usr/bin/env python

# encoding: utf-8

'''

@author: Roy Law

@license: (C) Copyright 2018.

@contact: https://github.com/RoyLaw

@file: quiz_json_fetcher.py

@time: 2018/1/13 上午1:21

@desc:

'''


import json
import requests
import time


def get_quiz():
    resp = requests.get('http://htpmsg.jiecaojingxuan.com/msg/current',timeout=4).text
    # resp = requests.get('http://wehave.love/current.json', timeout=4).text

    try:
        resp_dict = json.loads(resp)
    except:
        print('JSON decoding is error. Try it again.')
        time.sleep(1)
        get_quiz()
    else:
        if resp_dict['msg'] != 'no data':
            resp_dict = eval(str(resp))

            question = resp_dict['data']['event']['desc']
            question = question[question.find('.') + 1:question.find('?')]

            options = resp_dict['data']['event']['options']
            options = list(eval(options))
            # 对问题进行处理，提高关键字适配度
            # $question = str_replace("which of these", "what", $question);
            # $question = str_replace(" not ", " ", $question);
            # $question = str_replace(" never ", " ", $question);
            # $question = str_replace("\n", " ", $question);
        else:
            question = 'no_data'
            options = []
        return question, options


