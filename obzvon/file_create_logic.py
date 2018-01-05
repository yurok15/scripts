import datetime
import time
import os
import subprocess
import logging

router_a_ip = '10.78.99.196'
router_b_ip = '10.78.99.195'


def create_call_file(number):
    new_file = open('/var/spool/asterisk/outgoing/%s' % number, 'w+')
    new_file.write('''Channel: SIP/10.78.99.196/%s
MaxRetries: 0
Callerid: %s
RetryTime: 20
WaitTime: 20
Context: pa-system
Extension: 10
Priority: 1
''' % (number, number))
    os.chown('/var/spool/asterisk/outgoing/%s' % number, 995, 1000)
    logging.info( u'Call file for number %s was successfully created' % number)


def get_router(router_a):
    if router_a < 2:
        router_a += 1
        return router_a, router_a_ip
    else:
        router_a = 0
        return router_a, router_b_ip


def check_file_numbers():
    return len(os.listdir('/var/spool/asterisk/outgoing/'))


def check_call_numbers():
    call_numbers = subprocess.Popen(["asterisk -rx 'core show calls' | grep active | cut -d' ' -f1"], stdout=subprocess.PIPE, shell=True)
    (out, err) = call_numbers.communicate()
    return int(out)


def file_create_logic(phone_number):
    if datetime.date.weekday(datetime.date.today()) < 5:
        start_time = 8
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
                #router_a, ip = get_router(router_a)
                create_call_file(phone_number)
                break
    #return router_a