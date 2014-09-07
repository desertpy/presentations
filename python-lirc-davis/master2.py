#!/usr/bin/env python

import lirc

lstat = lirc.init('master2', '/etc/lirc/lircrc', 1)

while 1:
    x = lirc.nextcode()
    if x:
        k = x[0]
        print('from M2, you pressed: {}'.format(k))


