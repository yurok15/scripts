#!/usr/bin/python2.7
###########################################################
#
# This python script is used to generate asterisk call files
# into the directory /var/spool/asterisk/outgoing/
#
# Written by : Yuriy Zhigulskiy
# email: yurok15@gmail.com
# github: yurok15@gmail.com
# Created date: Dec 26, 2017
# Last modified: Jan 04, 2018
# Tested with : Python 2.7
# Script Revision: 0.5
# From revision 0.5 threading and statistics was added
#
##########################################################

from file_create_logic import *
import socket
from thread import start_new_thread

sock = socket.socket()
sock.bind(('127.0.0.1', 9090))
sock.listen(1)

#start_time = 0
#router_a = 0
#ip = ''
bad_numbers = 0
good_numbers = 0
data_list_len = []

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', filename="obzvon.log", level=logging.INFO)


def net_thread():
    global good_numbers
    global bad_numbers
    global data_list_len
    while True:
        conn, addr = sock.accept()
        conn.sendall("Good numbers: " + str(good_numbers) + "\n"
                     + "Bad numbers: " + str(bad_numbers) + "\n"
                     + "Total numbers: " + str(data_list_len) + "\n"
                     + "Done in %: " + str((good_numbers + bad_numbers)*100/data_list_len) + "%\n"
                     )
        conn.close()


def main_job(data_list):
    global bad_numbers
    global good_numbers
    global data_list_len
    data_list_len = len(data_list[0:])
    while data_list[0] != "":
        if int(len(data_list[0])) < 11:
            logging.warning(u'Bad number %s' % data_list[0])
            bad_numbers += 1
            data_list.remove(data_list[0])
        else:
            file_create_logic(data_list[0])
            good_numbers = good_numbers + 1
            data_list.remove(data_list[0])


def main():
    with open('test_numbers.txt') as file:
        read_data = file.read()
    data_list = read_data.split()
    start_new_thread(net_thread, ())
    start_new_thread(main_job(data_list),)


if __name__ == "__main__":
    main()
