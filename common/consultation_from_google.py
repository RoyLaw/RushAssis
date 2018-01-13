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
from googleapiclient.discovery import build
import socks
import socket


# Set SOCKS Proxy for Google Custom Search
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
socket.socket = socks.socksocket

# Google Custom Search
g_cse_api_key = 'key'
g_cse_id = 'id'


def google_search(query, start):
    service = build("customsearch", "v1", developerKey=g_cse_api_key)
    res = service.cse().list(q=query, cx=g_cse_id, start=start).execute()
    return res


def naive_approach(question):
    url = "https://www.google.com.tr/search?q={}".format(question)
    webbrowser.open(url)


# Google Question and count number of each result
def metric1Func(question, answers):
    met1 = [0, 0, 0]
    res = google_search(question, None)
    items = str(res['items']).lower()
    print(items)
    met1[0] = items.count(answers[0].lower())
    met1[1] = items.count(answers[1].lower())
    met1[2] = items.count(answers[2].lower())
    print(met1)
    return met1


# Google Question and each specific Answer and count total results
def metric2Func(question, answers):
    met2 = [0, 0, 0]
    res0 = google_search(question + ' "' + answers[0] + '"', None)
    res1 = google_search(question + ' "' + answers[1] + '"', None)
    res2 = google_search(question + ' "' + answers[2] + '"', None)
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
    met1 = metric1Func(question, options)
    met2 = metric2Func(question, options)
    return predict(met1, met2, options)
