#!usr/bin/env python

def inet_pton(str_ipv4):
    v =  [int(i) for i in str_ipv4.split('.')]
    return reduce(lambda x,y : x << 8 | y, reversed(v))


if __name__ == '__main__':
    v = inet_pton('192.168.1.22')
    print hex(v)
