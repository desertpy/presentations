#!/usr/bin/env python

from sys import argv

from redis import Redis
from rq import Queue

from count import count_words_at_url

q = Queue(connection=Redis())

if len(argv) > 1:
    result = q.enqueue(count_words_at_url, argv[1])
    print result
