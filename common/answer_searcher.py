#!/usr/bin/env python

# encoding: utf-8

'''

@author: Roy Law

@license: (C) Copyright 2018.

@contact: https://github.com/RoyLaw

@file: answer_searcher.py

@time: 2018/1/13 上午10:48

@desc:

'''

import webbrowser
import urllib
from common import consultation_from_google

questions = []
questions.append('no_data')
waiting_for_new_data = 0


def search_quiz(question, options):
    global waiting_for_new_data
    if question not in questions:
        waiting_for_new_data = 0
        questions.append(question)
        print('Questioning:' + question)
        webbrowser.open("https://www.google.com/search?source=hp&q=" + urllib.parse.quote(question))
        print(options)
        print(consultation_from_google.consult_google(question, options))
    elif waiting_for_new_data == 0:
        print('Waiting for any question...')
        waiting_for_new_data = 1
