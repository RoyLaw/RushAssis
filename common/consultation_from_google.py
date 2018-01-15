#!/usr/bin/env python

# encoding: utf-8

'''

@author: Roy Law

@license: (C) Copyright 2018.

@contact: https://github.com/RoyLaw

@file: consultation_from_google.py

@time: 2018/1/13 下午1:40

@desc:

@ref: https://developers.google.com/api-client-library/python/apis/customsearch/v1

'''

import webbrowser
import urllib
from googleapiclient.discovery import build
import socks
import socket
import threading

# Google Custom Search
g_cse_api_key = 'Your CSE API KEY'
g_cse_id = 'Your CSE ID'

g_cse_thread = []
g_cse_thread_m2 = []


class CSEThread(threading.Thread):
    def __init__(self, func, args=(), tid=-1):
        super(CSEThread, self).__init__()
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


def google_search(query, start):
    # Set SOCKS Proxy for Google Custom Search
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
    socket.socket = socks.socksocket

    service = build("customsearch", "v1", developerKey=g_cse_api_key)
    res = service.cse().list(q=query, cx=g_cse_id, start=start).execute()
    return res


def naive_approach(question):
    url = "https://www.google.com/search?source=hp&q=" + urllib.parse.quote(question)
    webbrowser.open(url)


# Google Question and count number of each result
def metric1Func(question, answers):
    met1 = [0, 0, 0]
    res = google_search(question, None)
    items = str(res['items']).lower()
    met1[0] = items.count(answers[0].lower())
    met1[1] = items.count(answers[1].lower())
    met1[2] = items.count(answers[2].lower())
    print('Google CSE Method 1: ' + str(met1))
    return met1


# Google Question and each specific Answer and count total results
def metric2Func(question, answers):
    # res0 = google_search(question + ' "' + answers[0] + '"', None)
    # res1 = google_search(question + ' "' + answers[1] + '"', None)
    # res2 = google_search(question + ' "' + answers[2] + '"', None)

    for i in range(3):
        t_m2 = CSEThread(google_search, args=(question.replace('_KEYWORD_', answers[i]) + ' ' + answers[i] + ' ', None),
                         tid=i)
        g_cse_thread_m2.append(t_m2)
        t_m2.start()
    for t_m2 in g_cse_thread_m2:
        t_m2.join()
        if t_m2.tid == 0:
            res0 = t_m2.get_result()
        elif t_m2.tid == 1:
            res1 = t_m2.get_result()
        elif t_m2.tid == 2:
            res2 = t_m2.get_result()

    print('Google CSE Method 2: ' + res0['searchInformation']['totalResults'] + ', ' + res1['searchInformation'][
        'totalResults'] + ', ' + res2['searchInformation']['totalResults'])

    return [int(res0['searchInformation']['totalResults']), int(res1['searchInformation']['totalResults']),
            int(res2['searchInformation']['totalResults'])]


def predict(metric1, metric2, answers):
    max1 = metric1[0]
    max2 = metric2[0]
    for x in range(1, 3):
        if metric1[x] > max1:
            max1 = metric1[x]
        if metric2[x] > max2:
            max2 = metric2[x]
    if metric1.count(0) == 3:
        return answers[metric2.index(max2)]
    elif metric1.count(max1) == 1:

        if metric1.index(max1) == metric2.index(max2):
            return answers[metric1.index(max1)]
        else:
            percent1 = max1 / sum(metric1)
            percent2 = max2 / sum(metric2)
            if percent1 >= percent2:
                return answers[metric1.index(max1)]
            else:
                return answers[metric2.index(max2)]
    elif metric1.count(max1) == 3:
        return answers[metric2.index(max2)]
    else:
        return answers[metric2.index(max2)]


def consult_google(question, options):
    # met1 = metric1Func(question, options)
    # met2 = metric2Func(question, options)
    met1 = met2 = options[0]
    t1 = CSEThread(metric1Func, args=(question, options), tid=1)
    g_cse_thread.append(t1)
    t2 = CSEThread(metric2Func, args=(question, options), tid=2)
    g_cse_thread.append(t2)
    t1.start()
    t2.start()
    for t in g_cse_thread:
        t.join()
        if t.tid == 1:
            met1 = t.get_result()
        elif t.tid == 2:
            met2 = t.get_result()
    return predict(met1, met2, options)
