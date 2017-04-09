#!/usr/bin/python

import bluetooth
import time

print "In/Out Board"

while True:
    print "Checking " + time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())

    result = bluetooth.lookup_name('C0:EE:FB:47:53:DE', timeout=5)
    if (result != None):
        print "present"
    else:
        print "not present"

    time.sleep(7)

