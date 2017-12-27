import logging
import os
import time
import datetime

logging.basicConfig(filename="obzvon.log", level=logging.INFO)

def create_call_file(number):
    new_file = open('/var/tmp/numbers/%s' %number, 'w+')
    new_file.write('''Channel: SIP/10.78.99.196/%s
MaxRetries: 1
RetryTime: 30
WaitTime: 30
Context: pa-system
Extension: 10
Priority: 1
''' % (number))

def check_file_numbers():
    return(len(os.listdir('/var/tmp/numbers')))

def main():
    with open('new_number2.txt') as file:
        read_data = file.read()
    data_list = read_data.split()
    for phone_number in data_list:
        if int(len(phone_number)) < 11:
            print('Bad number %s' % (phone_number))
        else:
            #check current time
            now = datetime.datetime.now()
            if now.hour > 11 and now.hour < 18:
                # check file numbers in directory
                if check_file_numbers() < 10:
                    #create call file
                    create_call_file(phone_number)
                else:
                    time.sleep(2)
            else:
                print("Not running time")
                time.sleep(60)


if __name__ == "__main__":
    main()
