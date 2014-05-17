#!/usr/bin/env python
#coding:utf-8

import types
import copy
import itertools
import time

class RoundRobin(object):
    """
    Help on class RoundRobin:
    NAME
        RoundRobin - implement of round robin algorithm.
    FILE
        RoundRobin.py
    DESCRIPTION
        rr = RoundRobin(scope)
        rr is a callable object with next, iter, send interface.
        scope is round robin algorithm's input parameter
        if scope is 4, loop in [0, 1, 2, 3]
        if scope is list or tuple, loop in it
    """

    def _init(self, scope):
        if type(scope) is types.IntType:
            self._scope = [i for i in xrange(scope)]
        elif type(scope) is types.ListType or type(scope) is types.TupleType:
            self._scope = copy.deepcopy(scope)
        else:
            self._scope = None
            raise ValueError('Parameter scope in constructor must be int, list or tuple\n')
        self._item = itertools.cycle(self._scope)
        self._size = len(self._scope)
        self._index = 0

    def __init__(self, scope):
        '''Constructor,scope can be number,list or tuple'''
        self._init(scope)

    def next(self):
        '''obj.next() return next val in round robin scope like yield object'''
        return self._item.next()

    def send(self, scope):
        '''obj.send(r) send a new scope to round robin like yield object'''
        if scope is not None:
            self._init(scope)
            return self._item.next()
        else:
            return self._item.next()

    def reset(self):
        '''obj.reset() reset round robin count'''
        self._item = itertools.cycle(self._scope)

    def close(self):
        '''obj.close() close round robin algorithm like yield object'''
        self._item = iter([])

    def __iter__(self):
        '''iter(obj) return iterator of round robin scope'''
        return self._item

    def __next__(self):
        '''next(obj) implement next(obj) interface, return iterator like yield object'''
        return iter(self)

    def __call__(self):
        '''__call__ return real yield object. this is very slow!!!'''
        def _rryield():
            while True:
                self._index %= self._size
                newarg = (yield self._scope[self._index])
                self._index += 1
                if newarg is not None:
                    self._init(newarg)
        return _rryield()



def rrtest():
    print '\ntest list'
    rr1 = RoundRobin(['aa', 'bb', 'cc'])
    it = iter(rr1)
    print next(it)  #use system interface
    print next(it)
    print next(it)
    print next(it)

    print '\ntest tuple'
    rr2 = RoundRobin(('11', '22', '33'))
    print rr2.next()    #use member function
    print rr2.next()
    print rr2.next()
    print rr2.next()
    #if need to send new param
    print rr2.send([7,8,9])
    print rr2.send(None)
    rr2.close()     #test close
    try:
        print rr2.next()
    except StopIteration, e:
        pass


    print '\ntest number'
    ry = RoundRobin(4)() #get real genarator object
    print next(ry)
    #if need to reset
    print next(ry)
    print ry.next()
    print ry.next()
    print ry.next()
    print ry.next()
    print ry.send([55,66])
    print ry.send(None)
    print ry.send(None)
    ry.close()

    print '\ntest using in for loop'
    k = 5 #test 5 times
    for i in RoundRobin(4): #using as iterator
        print i
        k -= 1
        if 0 == k:
            break
    print



if __name__ == '__main__':
    print help(RoundRobin)
    print 'test RoundRobin'
    rrtest()
    print 'test success'

    #测试仿真协程性能
    t1 = time.clock()
    for i in xrange(1,1000):
        r = RoundRobin(i)
        for j in xrange(1,10000):
            r.next()
    print 'using native method:', time.clock() - t1,'s'

    #测试真实协程性能
    t2 = time.clock()
    for i in xrange(1,1000):
        r = RoundRobin(i)
        y = r()
        for j in xrange(1,10000):
            y.next()
    print 'using real yield:', time.clock() - t2,'s'
    
