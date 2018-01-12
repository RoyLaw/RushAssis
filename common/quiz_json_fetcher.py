#!/usr/bin/env python

# encoding: utf-8

'''

@author: Roy Law

@license: (C) Copyright 2018.

@contact: roy.law@qq.com

@file: quiz_json_fetcher.py

@time: 2018/1/13 上午1:21

@desc:

'''

import json
import requests
import webbrowser
import urllib

questions = []


def get_answer():
    # resp = requests.get('http://htpmsg.jiecaojingxuan.com/msg/current',timeout=4).text
    resp = requests.get('http://wehave.love/current.json',timeout=4).text
    resp_dict = json.loads(resp)
    if resp_dict['msg'] == 'no data':
        return 'Waiting for a question...'
    else:
        resp_dict = eval(str(resp))

        question = resp_dict['data']['event']['desc']
        question = question[question.find('.') + 1:question.find('?')]

        options = resp_dict['data']['event']['options']

        list(options)
        for x in options:
            print(x)

        # print(options)

        if question not in questions:
            questions.append(question)
            webbrowser.open("https://www.google.com/search?source=hp&q=" + urllib.parse.quote(question))
        else:
            return 'Waiting for new questions...'
