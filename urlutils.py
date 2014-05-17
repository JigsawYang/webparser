#!/usr/bin/env python
#coding:utf-8
## auther : jerry chen
## date   : 2014.5.16

import urllib, urllib2, urlparse
import socket
import os
import StringIO

try:
    import pycurl
except ImportError, e:
    print 'Can\'t find Lib pycurl!'
    raise e


Accept = '*/*'
Accept_Lang = 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0'



def _url_open(urlstr, callback):
    '''Inner function, implement open URL and deal respone with callback fun'''
    try:
        req = urllib2.Request(urlstr)
        #print req
        req.add_header('Accept', Accept)
        req.add_header('Accept-Language', Accept_Lang)
        req.add_header('User-Agent', User_Agent)
        respone = urllib2.urlopen(req);
        #print respone
        data = respone.read()
        if data:
            return callback(data)
        else:
            #if __debug__:
                #print urlstr, "failed!"
            return None
    except Exception, e:
        #print 'URL Exception:', e, 'from', urlstr[0:30], '...'
        return None



def open_urllist(urllist, callback, timeout = 1):
    '''Check every url in urllist and finally return a result list
       urllist  :a list of URL strings like ['http://www.baidu.com', 'http://www.google.com.hk', ...]
       callbask :user's function to deal with the respone of request
       timeout  :the socket's connection limit alive time
    '''
    assert urllist
    socket.setdefaulttimeout(timeout)

    size = len(urllist)
    result = [0] * size

    for i in xrange(size):
        #call inner function to deal with every url string
        result[i] = _url_open(urllist[i], callback)
        if (i % 100) == 0:
            print 'Process', os.getpid(), 'has finished ' + str(100.0*i/float(size)) + r'%'

    print 'Process', os.getpid(), 'has finished 100%'

    return result



def open_urllist_curl(urllist, callback, timeout = 1):
    '''Check every url in urllist and finally return a result list by libcurl or pycurl
       urllist  :a list of URL strings like ['http://www.baidu.com', 'http://www.google.com.hk', ...]
       callbask :user's function to deal with the respone of request
       timeout  :the socket's connection limit alive time
    '''
    curl = pycurl.Curl()
    s = pycurl.CurlShare()
    s.setopt(pycurl.SH_SHARE, pycurl.LOCK_DATA_COOKIE)
    s.setopt(pycurl.SH_SHARE, pycurl.LOCK_DATA_DNS)
    
    curl.setopt(pycurl.SHARE, s)
    curl.setopt(pycurl.URL, urllist[0])
    curl.setopt(pycurl.VERBOSE, 0)
    curl.setopt(pycurl.FOLLOWLOCATION, 0)
    curl.setopt(pycurl.DNS_CACHE_TIMEOUT, 3600) #Very important
    curl.setopt(pycurl.DNS_USE_GLOBAL_CACHE, 1) #Very important
    curl.setopt(pycurl.CONNECTTIMEOUT, 60)      #60 seconds OK?
    curl.setopt(pycurl.TIMEOUT, timeout)
    curl.setopt(pycurl.FRESH_CONNECT, 1)
    curl.setopt(pycurl.FORBID_REUSE, 0)
    curl.setopt(pycurl.HTTPHEADER, ['Accept: ' + Accept, 
                                    'Accept-Language: ' + Accept_Lang])
    curl.setopt(pycurl.USERAGENT, User_Agent)
    curl.setopt(pycurl.MAXREDIRS, 5)

    size = len(urllist)
    result = [0] * size

    for i in xrange(size):
        try:
            sio = StringIO.StringIO()

            curl.setopt(pycurl.WRITEFUNCTION, sio.write)
            curl.setopt(pycurl.URL, urllist[i])

            curl.perform()

            if __debug__ and curl.getinfo(pycurl.HTTP_CODE) != 200:
                print 'URL Exception: from', urllist[i][0:30], '...'

            result[i] = callback(sio.getvalue())

        except Exception, e:
            #print 'URL Exception:', e, 'from', urllist[i][0:30], '...'
            result[i] = None

        if (i % 100) == 0:
            print 'Process', os.getpid(), 'has finished ' + str(100.0*i/float(size)) + r'%'

    print 'Process', os.getpid(), 'has finished 100%'#, result

    curl.close()    #Never forget this!
    return result



if __name__ == '__main__':
    print help(open_urllist)
    print help(open_urllist_curl)


