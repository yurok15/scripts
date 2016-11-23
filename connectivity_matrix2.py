#!/usr/bin/python

import pwd
import os
import re
import glob
import time


PROC_TCP = "/proc/net/tcp"
STATE = {
        '01':'ESTABLISHED',
        '02':'SYN_SENT',
        '03':'SYN_RECV',
        '04':'FIN_WAIT1',
        '05':'FIN_WAIT2',
        '06':'TIME_WAIT',
        '07':'CLOSE',
        '08':'CLOSE_WAIT',
        '09':'LAST_ACK',
        '0A':'LISTEN',
        '0B':'CLOSING'
        }

def _hex2dec(s):
    return str(int(s,16))

def _load():
    ''' Read the table of tcp connections & remove header  '''
    with open(PROC_TCP,'r') as f:
        content = f.readlines()
        content.pop(0)
    return content

def _convert_ip_port(array):
    host,port = array.split(':')
    return _ip(host),_hex2dec(port)

def _remove_empty(array):
    return [x for x in array if x !='']

def _ip(s):
    ip = [(_hex2dec(s[6:8])),(_hex2dec(s[4:6])),(_hex2dec(s[2:4])),(_hex2dec(s[0:2]))]
    return '.'.join(ip)

def netstat(result):
  PERIOD_OF_TIME = 10  
  start = time.time()
  remote_hp = [] # Remote hp - host and port
  while True:
      content=_load()
      for line in content:
          line_array = _remove_empty(line.split(' '))
          l_host,l_port = _convert_ip_port(line_array[1]) # Convert ipaddress and port from hex to decimal.
          r_host,r_port = _convert_ip_port(line_array[2])
          if l_host == '0.0.0.0' or r_host == '0.0.0.0':
              continue
 	  else:
	      if "r_host':'r_port" not in remote_hp:
	           remote_hp.append("r_host':'r_port")
	           nline = [l_host+':'+l_port + ' --- ' +r_host+':'+r_port]
		   print(remote_hp)
	      else:
	          continue
      time.sleep(2)
      result.append(nline)
#      time.sleep(60)
      if time.time() > start + PERIOD_OF_TIME : break
  for i in range(len(result)):
      print(result[i])  # Print result
  return result



if __name__ == '__main__':
    result = []
    netstat(result)
        
