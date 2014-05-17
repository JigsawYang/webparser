#!/usr/bin/env python
#coding:utf-8
## auther : jerry chen
## date   : 2014.5.16

import re


IS_JS = 1
NOT_JS = 0

_jsurl = re.compile('.*?\.js\?.*')


def checkisjs_dynamic(resstr):
    '''check respone is javascript file or not'''
    pos = resstr.find('function')
    if pos > -1 and pos < 10:
        return IS_JS
    else:
        return NOT_JS


def checkisjs_static(urlstr):
    '''check respone is javascript file or not'''
    if _jsurl.match(urlstr):
        return IS_JS
    else:
        return NOT_JS