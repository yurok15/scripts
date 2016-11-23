#!/usr/bin/python
'''
This script login to the mailbox using secure connection and delete files
'''
import imaplib
import sys, getopt
from email.parser import HeaderParser
server = " "
username = " "
password = " "
mailbox_dir = " "


def main(argv):
    server = " "
    username = " "
    password = " "
    mailbox_dir = " "
    try:
        opts, args = getopt.getopt(argv,"hs:u:p:m:",["server=","username=","password=","mailbox="])
    except getopt.GetoptError:
        print 'delete_imap_msg.py -s <server> -u <username> -p <password> -m <mailbox>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ("Not correct")
            sys.exit()
        elif opt in ("-s", "--server"):
            server = arg
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "password"):
            password = arg
        elif opt in ("-m", "--mailbox"):
            mailbox_dir = arg

    m = imaplib.IMAP4_SSL(server)
    m.login(username, password)
    # get list of mailboxes
    list = m.list();
    # select which mail box to process
    m.select(mailbox_dir) 
    resp, data = m.uid('search',None, "ALL") # search and return Uids
    uids = data[0].split()    
    mailparser = HeaderParser()
    for uid in uids:
        resp,data = m.uid('fetch',uid,"(BODY[HEADER])")        
        msg = mailparser.parsestr(data[0][1])       
        print (msg['From'],msg['Date'],msg['Subject'])        
        print (m.uid('STORE',uid, '+FLAGS', '(\\Deleted)'))
    print (m.expunge())
    m.close() # close the mailbox
    m.logout()# logout

if __name__ == "__main__":
   main(sys.argv[1:])
