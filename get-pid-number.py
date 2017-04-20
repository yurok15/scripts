#!/usr/bin/python2.7
###########################################################
#
# This python script is used to get number of pid currently running on system
#
#
# Written by : Yuriy Zhigulskiy
# Created date: Apr 19, 2017
# Last modified: Apr 19, 2017
# Tested with : Python 2.7.6
# Script Revision: 0.1
#
##########################################################

import os
import sys

def main(argv):
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    number=0
    service_name=argv
    for p in pids:
        pid_name=open(os.path.join('/proc', p, 'comm'), 'rb').read().splitlines()
        pid=pid_name
        if pid == service_name:
            number+=1
        else:
            continue
    print(number)

if __name__ == "__main__":
    main(sys.argv[1:])
