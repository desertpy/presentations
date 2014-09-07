#!/usr/bin/env python

import lirc

lstat = lirc.init('master', '/etc/lirc/lircrc', 1)

while 1:
    x = lirc.nextcode()
    if x:
        k = x[0]
        print('you pressed: {}'.format(k))


