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
    header = {
        'X-Live-Device-Identifier': 'your id',
        'Accept': '*/*',
        'X-Live-Session-Token': 'your token',
        'X-Live-Device-Type': 'ios',
        'X-Live-OS-Version': 'Version 11.2.2 (Build 15C202)',
        'Accept-Language': 'en-HK;q=1.0, zh-Hans-HK;q=0.9, ja-HK;q=0.8, zh-Hant-HK;q=0.7, es-ES;q=0.6',
        'X-Live-App-Version': '1.0.4',
        'User-Agent': 'LiveTrivia/1.0.4 (com.chongdingdahui.app; build:0.1.7; iOS 11.2.2) Alamofire/4.6.0',
        'Content-Type': 'application/json',
    }
    resp = requests.get('http://msg.api.chongdingdahui.com/msg/current', headers=header, timeout=4).text


    try:
        resp_dict = json.loads(resp)
    except:
        print('JSON decoding is error. Try it again.')
        time.sleep(1)
        get_quiz()
    else:
        if resp_dict['msg'].strip() != 'no data':
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


