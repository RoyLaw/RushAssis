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


questions = []
questions.append('no_data')


def search_quiz(question, options):
    if question not in questions:
        questions.append(question)
        webbrowser.open("https://www.google.com/search?source=hp&q=" + urllib.parse.quote(question+options[0]))
    else:
        print('Waiting for any question...')
