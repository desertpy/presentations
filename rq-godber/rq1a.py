#!/usr/bin/env python

# python ./rq1a.py http://uberhip.com 192.168.59.103

from sys import argv

from redis import Redis
from rq import Queue

from count import count_words_at_url

if len(argv) > 2:
    q = Queue(connection=Redis(argv[2]))
    result = q.enqueue(count_words_at_url, argv[1])
    print result
else:
    print "Specify URL to count and REDIS server IP as arguments:"
    print "    python ./rq1a.py URL REDIS_IP"
    print "  e.g.:"
    print "    python ./rq1a.py http://uberhip.com 192.168.59.103"
