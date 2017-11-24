#!/usr/bin/python

with open('/etc/postfix/mynetworks', 'r') as file:
    read_data = file.read()
file.close

def printresult(position, ip):
    begin_position = 0
    end_position = 0
    while True:
        symbol = read_data[position]
        if '#' == read_data[position]:
            begin_position = position
            while True:
                position = position + 1
                if '\n' == read_data[position]:
                    end_position = position
                    break
                else:
                    continue
            print(read_data[begin_position:end_position], ip)
            break
        else:
            position = position - 1
            continue

with open('/var/tmp/cust.txt') as cust_file:
    cust_data = cust_file.read()
cust_file.close()


for ip in cust_data.splitlines():
    position = read_data.find(ip)
    printresult(position, ip)
