#!/usr/bin/env python
#coding:utf-8

try:
    import hashlib
    import zlib
    import base64
except ImportError, e:
    print 'SimpleCrypt need Python2.7\n'
    raise e

class SimpleCrypt(object):
    """
    Help on class SimpleCrypt:
    CLASS
        SimpleCrypt
    FILE
        SimpleCrypt.py
    DESCRIPTION
        eg:
        a = SimpleCrypt()
        print a.md5('asd')
    """

    def __init__(self):
        """Constructer, nothing to do..."""
        pass

    def _hashfun(self, data, hashfun, bufsize):
        """inner function, you should never using this..."""
        h = None
        try:
            h = getattr(hashlib, hashfun)()
            h.update(data.read())
            while True:
                b = data.read(bufsize)
                if not b:
                    break;
                h.update(b)
            return h.hexdigest().upper()
        except AttributeError, e:
            h.update(data)
            return h.hexdigest().upper()
        except IOError, e:
            print 'SimpleCrypt: IOError happend when reading date...\n'
        except Exception, e:
            print e
            print 'SimpleCrypt: get %s val failed' % hashfun


    def md5(self, data, bufsize = 2048):
        """return sha1 val of data, accept a string or a readable object"""
        return self._hashfun(data, self.md5.__name__, bufsize)

    def sha1(self, data, bufsize = 2048):
        """return sha1 val of data, accept a string or a readable object"""
        return self._hashfun(data, self.sha1.__name__, bufsize)

    def sha256(self, data, bufsize = 2048):
        """return sha256 val of data, accept a string or a readable object"""
        return self._hashfun(data, self.sha256.__name__, bufsize)

    def sha512(self, data, bufsize = 2048):
        """return sha512 val of data, accept a string or a readable object"""
        return self._hashfun(data, self.sha512.__name__, bufsize)

    def crc32(self, data):
        """return crc32 checksum of data, accept a string object"""
        try:
            return zlib.crc32(data)
        except Exception, e:
            print 'SimpleCrypt: crc32 accept a string object'

    def base64_encode(self, data):
        """return base64 encode string of data, accept a string object"""
        try:
            return base64.b64encode(data)
        except Exception, e:
            print 'SimpleCrypt: base64_encode accept a string object'

    def base64_decode(self, data):
        """return base64 decode string of data, accept a string object"""
        try:
            return base64.b64decode(data)
        except Exception, e:
            print 'SimpleCrypt: base64 decode accept a encoded string object'


if __name__ == '__main__':
    if __debug__:
        teststr = 'Hello Python!'
        a = SimpleCrypt()
        #print help(a)
        print 'md5:', a.md5(teststr)
        print 'sha1:', a.sha1(teststr)
        print 'sha256:', a.sha256(teststr)
        print 'sha512:', a.sha512(teststr)
        print 'crc32:', a.crc32(teststr)
        en = a.base64_encode(teststr)
        print 'base64 encode:', en
        print 'base64 decode:', a.base64_decode(en)
        import sys
        with open(sys.argv[0]) as f:
            print 'md5', a.md5(f)
        print '\nTest of SimpleCrypt Successed!\n'