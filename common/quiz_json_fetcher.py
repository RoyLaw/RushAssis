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
import webbrowser
import urllib

questions = []
questions.append('no_data')


def get_quiz():
    # resp = requests.get('http://htpmsg.jiecaojingxuan.com/msg/current',timeout=4).text
    resp = requests.get('http://wehave.love/current.json', timeout=4).text

    try:
        resp_dict = json.loads(resp)
    except:
        print('JSON decoding is error. Try it again.')
        get_quiz()
    else:
        if resp_dict['msg'] != 'no data':
            resp_dict = eval(str(resp))

            question = resp_dict['data']['event']['desc']
            question = question[question.find('.') + 1:question.find('?')]

            options = resp_dict['data']['event']['options']
            options = list(eval(options))
        else:
            question = 'no_data'
            options = []
        return question, options


def search_quiz(question, options):
    if question not in questions:
        questions.append(question)
        webbrowser.open("https://www.google.com/search?source=hp&q=" + urllib.parse.quote(question+options[0]))
    else:
        print('Waiting for any question...')
