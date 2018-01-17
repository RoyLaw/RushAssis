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

from common import consultation_from_google
from common import consultation_from_baidu
import threading
import time

questions = []
questions.append('no_data')
waiting_for_new_data = 0


class ASThread(threading.Thread):
    def __init__(self, func, args=(), tid=-1):
        super(ASThread, self).__init__()
        self.func = func
        self.args = args
        self.tid = tid

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None


def search_quiz(question, options):
    global waiting_for_new_data
    if question not in questions:
        waiting_for_new_data = 0
        questions.append(question)

        # st = time.time()
        print('\nQuestioning: ' + question)
        question = optimize_question(question)
        consultation_from_google.naive_approach(optimize_question(question))
        print('Options: ' + str(options))

        t1 = ASThread(google_result_print, args=(question, options))
        t2 = ASThread(baidu_result_print, args=(question, options))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # google_result_print(question,options)
        # baidu_result_print(question,options)

        # print(time.time()-st)

    elif waiting_for_new_data == 0:
        print('Waiting for new question...')
        waiting_for_new_data = 1


def google_result_print(question, options):
    print('Google\'s Suggestion: ' + consultation_from_google.consult_google(question, options))


def baidu_result_print(question, options):
    print('Baidu\'s Suggestion: ' + str(consultation_from_baidu.baidu_count(question, options)))


def optimize_question(question, type='general'):
    if '不是' in question:
        print('***此题为否定题***')
    if type == 'google':
        question = question.replace('不', '')
        question = question.replace('哪个', '_KEYWORD_')
        question = question.replace('没', '')
        question = question.replace('几', '_KEYWORD_')
        question = question.replace('谁', '_KEYWORD_')
        question = question.replace('什么', '_KEYWORD_')
        question = question.replace('哪项', '_KEYWORD_')
        question = question.replace('哪种', '_KEYWORD_')
        question = question.replace('哪里', '_KEYWORD_')
        question = question.replace('哪位', '_KEYWORD_')
    else:
        question = question.replace('不', '')
        question = question.replace('哪个', ' ')
        question = question.replace('没', '')
        question = question.replace('几', ' ')
        question = question.replace('谁', ' ')
        question = question.replace('什么', ' ')
        question = question.replace('哪项', ' ')
        question = question.replace('哪项', ' ')
        question = question.replace('哪种', ' ')
        question = question.replace('哪里', ' ')
        question = question.replace('哪位', ' ')
    return question
