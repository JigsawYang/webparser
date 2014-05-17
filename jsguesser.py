#!/usr/bin/env python
#coding:utf-8
## auther : jerry chen
## date   : 2014.5.16

import os, sys
import multiprocessing
import time

try:
    import urlutils
    import www_duba_com as duba
except ImportError, e:
    print 'Can\'t find module urlutils!'
    raise e


checkisjs_dynamic = duba.checkisjs_dynamic
checkisjs_static = duba.checkisjs_static
IS_JS = duba.IS_JS


PROT_PREFIX = 'http://' #protocal prefix of url string


def _addprot(line):
    '''if the url string start from www... or others, then add protocal "http://" is necessary'''
    if line[0:7] != PROT_PREFIX:
        return PROT_PREFIX + line
    else :
        return line



def _jsguess_task(urllist, path_output, timeout):
    '''analyze file form path_input and create a result file named path_output'''
    try:
        print len(urllist), "urls to be analyze\n"

        #check if windows utf-8 format file
        if urllist[0][0] == '\xef' and urllist[0][1] == '\xbb' and urllist[0][2] == '\xbf':
            urllist[0] = urllist[0][3:]

        urllist = map(_addprot, urllist) #add http:// prefix
        result = urlutils.open_urllist_curl(urllist, checkisjs_dynamic, timeout)
        #print result
        assert len(result) == len(urllist)

        with open(path_output, 'w') as resultfile:
            for i in zip(result, urllist):
                if IS_JS == i[0]:
                    resultfile.write(i[1])

    except Exception, e:
        print e
        print 'jsguesser failed!\r\n'



#########################################################################
STEPPER = 300  #open new process when number of url larger then this val
#########################################################################


def jsguess_run_dynamic(arg):
    '''run jsguesser by multi process'''
    try:
        with open(arg[1], 'r') as f:
            urllist = f.readlines()

        begin = 0;  end = STEPPER   
        fileid = 0
        proclist = [];  
        outputs = []

        #analysis input file and create processes
        while begin < len(urllist):
            output = arg[1] + '-' + str(fileid)
            outputs.append(output)
            a = (urllist[begin:end], output, int(arg[2]))
            #create new process
            proclist.append(multiprocessing.Process(target = _jsguess_task, args = a))
            print 'Process', proclist[-1].pid, 'started...'
            proclist[-1].start()
            begin += STEPPER
            end += STEPPER
            fileid += 1

        #waiting for every process finish...
        time.sleep(1)
        for i in proclist:
            i.join()
            print i, "joined"

        #post process, merge result files
        result_file = arg[1] + '.result'
        with open(result_file, 'w') as f:
            for i in outputs:
                with open(i, 'r') as o:
                    f.writelines(o.readlines())
                os.remove(i)

        return result_file

    except Exception, e:
        print e
        print 'Usage: python jsguesser.py file 5.0'
        print 'file is your url record file with full path, 5.0 is tcp time out'



def jsguess_run_static(arg):
    '''run jsguesser '''
    try:
        with open(arg[1], 'r') as f:
            urllist = f.readlines()

        result_file = arg[1] + '.result'

        with open(result_file, 'w') as f:
            for i in urllist:
                if checkisjs_static(i) == IS_JS:
                    f.write(i)
                    f.flush()

        return result_file

    except Exception, e:
        print e
        print 'Usage: python jsguesser.py file 5.0'
        print 'file is your url record file with full path, 5.0 is tcp time out'



def sort_result(rfile):
    '''sort results in rfile'''
    with open(rfile, 'r') as f:
        lines = f.readlines()

    sortedlist = lines
    sortedlist.sort()

    merged = dict()
    for i in sortedlist:
        if i in merged:
            merged[i] += 1
        else:
            merged[i] = 1

    with open(rfile+'2', 'w') as f:
        f.write('Rank  Times  URL\n')
        n = 0
        for i in sorted(merged.items(), key=lambda d:d[1], reverse=True):
            n += 1
            f.write('%4d  ' % n)
            f.write('%5d  ' % i[1])
            f.write(i[0])



if __name__ == '__main__':
    t1 = time.ctime()
    #result_file = jsguess_run_dynamic(sys.argv)
    result_file = jsguess_run_static(sys.argv)
    if result_file:
        sort_result(result_file)
        print '\nAll Success!!!'
        t2 = time.ctime()
        print 'start time : ', t1
        print 'end time : ', t2






