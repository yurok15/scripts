#!/usr/bin/python2.7
###########################################################
#
# This python script is used to generate asterisk call files
#
# Written by : Yuriy Zhigulskiy
# email: yurok15@gmail.com
# github: yurok15@gmail.com
# Created date: Dec 26, 2017
# Last modified: Dec 29, 2017
# Tested with : Python 2.7
# Script Revision: 0.3
#
##########################################################

import logging
import os
import time
import datetime
import subprocess

start_time = 0
#end_time = 20
router_a_ip = '10.78.99.196'
router_b_ip = '10.78.99.195'
router_a = 0
ip = ''

logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', filename="obzvon.log", level=logging.INFO)

def create_call_file(number, ip):
    new_file = open('/var/spool/asterisk/outgoing/%s' %number, 'w+')
    new_file.write('''Channel: SIP/%s/%s
MaxRetries: 0
Callerid: %s
RetryTime: 20
WaitTime: 20
Context: pa-system
Extension: 10
Priority: 1
''' % (ip, number, number))
    os.chown('/var/spool/asterisk/outgoing/%s' %number, 995, 1000)
    logging.info( u'Call file for number %s, got to router (%s) was successfully created' % (number, ip))

def check_file_numbers():
    return(len(os.listdir('/var/spool/asterisk/outgoing/')))

def check_call_numbers():
    call_numbers = subprocess.Popen(["asterisk -rx 'core show calls' | grep active | cut -d' ' -f1"], stdout=subprocess.PIPE, shell=True)
    (out, err) = call_numbers.communicate()
    return(int(out))

def get_router(router_a):
    if router_a < 2:
        router_a += 1
        #print("a")
        return(router_a, router_a_ip)
    else:
        router_a = 0
        #print("b")
        return(router_a, router_b_ip)

def file_create_logic(phone_number, router_a, ip):
    if datetime.date.weekday(datetime.date.today()) < 5:
        start_time = 11
    else:
        start_time = 14
    while True:
        now = datetime.datetime.now()
        if now.hour < start_time or now.hour > 19:
            logging.warning( u'Bad time for customer call')
            time.sleep(10)
            continue
        else:
            if check_file_numbers() > 11: #or check_call_numbers() > 10:
                time.sleep(2)
                continue
            else:
                ###
                ### function to get next hop VOIP router
                ###
                router_a, ip = get_router(router_a)
                create_call_file(phone_number, ip)
                break
    return(router_a)


def main(router_a):
    with open('test_numbers.txt') as file:
        read_data = file.read()
    data_list = read_data.split()
    for phone_number in data_list:
        if int(len(phone_number)) < 11:
            logging.warning( u'Bad number %s' % (phone_number))
        else:
            router_a = file_create_logic(phone_number, router_a, ip)


if __name__ == "__main__":
    main(router_a)
