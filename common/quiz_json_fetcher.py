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
        'X-Live-Device-Identifier': 'Your Device Id',
        'Accept': '*/*',
        'X-Live-Session-Token': 'Your Session Token',
        'X-Live-Device-Type': 'ios',
        'X-Live-OS-Version': 'Version 11.2.2 (Build 15C202)',
        'Accept-Language': 'en-HK;q=1.0, zh-Hans-HK;q=0.9, ja-HK;q=0.8, zh-Hant-HK;q=0.7, es-ES;q=0.6',
        'X-Live-App-Version': '1.0.4',
        'User-Agent': 'LiveTrivia/1.0.4 (com.chongdingdahui.app; build:0.1.7; iOS 11.2.2) Alamofire/4.6.0',
        'Content-Type': 'application/json',
    }

    resp = requests.get('http://msg.api.chongdingdahui.com/msg/current', headers=header, timeout=4).text

    try:
        resp_dict = json.loads(json_format(resp))
    except:
        print('JSON decoding is error. Try it again.')
        time.sleep(1)
    else:
        if resp_dict['msg'].strip() != 'no data':
            resp_dict = eval(str(resp))

            question = resp_dict['data']['event']['desc']
            question = question[question.find('.') + 1:question.find('?')]

            options = resp_dict['data']['event']['options']
            options = list(eval(options))
        else:
            question = 'no_data'
            options = []
        return question, options
    get_quiz()


# Keep JSON Data Safe from Quota Marks
def json_format(json_resp):
    json_temp = str(json_resp)
    for i in range(len(json_temp) - 2):
        if json_temp[i] == ':' and json_temp[i + 1] == '"':
            for j in range(i + 2, len(json_resp)):
                if json_temp[j] == '"':
                    if json_temp[j + 1] != ',' and json_temp[j + 1] != '}' and json_temp[j - 1] != '[' \
                            and json_temp[j + 1] != ']':
                        json_temp = json_temp[:j - 1] + '“' + json_temp[j + 1:]
                    elif json_temp[j + 1] == ',' or json_temp[j + 1] == '}':
                        break
    return json_temp
