#!/usr/bin/env python
import sys, csv
import telnetlib
import xml.etree.ElementTree as ET
import string
from random import sample, choice

tn = telnetlib.Telnet('localhost','3333')
tn.write("new Imedia::HP::Postfix({userName=>q{FlywheelSports},domain=>q{flywheelsports.com}}) \n")
s=tn.read_until("</rppcEval>")
root = ET.fromstring(s.strip())
obj = root.find('return').text
if root.find('errCode').text != '0' or not obj:
  sys.exit("Unable to get rppcd object"+s)

chars = string.letters + string.digits

f=open('list.csv','rb')
reader = csv.reader(f,delimiter=';')
for row in reader:
  if len(row)<3:
    print "Invalid line: %s" % row
    continue
  fullname=row[1].strip()
  login=row[0].strip()
  password=''.join([choice(chars) for i in range(8)])
  #password=row[2].replace('{','\{').replace('}','\}')
  if '@' in login: login=login.split('@')[0]
  if not login or not password or not fullname:
    print "Invalid line: %s" % row
    continue

  print "%s;%s;%s"%(fullname,login,password)
  if ' ' in login or "'" in login:
    print "Invalid chars in login"
    continue
  tn.write("%s->addMailbox(q{%s}, q{%s}, q{}, q{6000}) \n"%(obj, login, password) )
  s=tn.read_until("</rppcEval>")
  root = ET.fromstring(s.strip())
  if root.find('return').text!='1' or root.find('errCode').text!='0':
    print "Error while creating mailbox %s: %s"%(login, s)
    continue

  tn.write("%s->setMailboxFullName(q{%s},q{%s}) \n"%(obj, login, fullname) )
  s=tn.read_until("</rppcEval>")
  root = ET.fromstring(s.strip())
  if root.find('return').text!='1' or root.find('errCode').text!='0':
    sys.exit("Error while setting name for mailbox %s: %s"%(login, s))