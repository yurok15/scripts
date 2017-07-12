#!/usr/bin/python2.7
###########################################################
#
# This python script is used to generate easyJet report
# FP: 2575728
#
# Written by : Yuriy Zhigulskiy
# Created date: Apr 25, 2017
# Last modified: Apr 26, 2017
# Tested with : Python 2.7.6
# Script Revision: 0.4
#
##########################################################

import ldap.modlist as modlist
import time
import datetime
import os
from datetime import datetime
import csv
import ldap
import logging
import subprocess

logging.basicConfig(filename="/var/log/easyjet-report.log", level=logging.INFO)
REPORT_FILE="easyjet-report"
REPORT_F="/var/tmp/easyjet_report"+"_"+datetime.now().strftime("%d_%m_%Y")

def main():
    #LDAP connection
    l = ldap.initialize("ldap://ldap.exch500.serverdata.net:389/")
    l.simple_bind_s("ADPostfixLDAPSvc@exch500.msoutlookonline.net", "vgy7gr39juhaejawe5hg534y45tgw45f")
    baseDN = "OU=easyJet,OU=Hosting,DC=exch500,DC=msoutlookonline,DC=net"
    searchScope = ldap.SCOPE_SUBTREE
    retrieveAttributes=('displayName', 'cn', 'targetAddress', 'hostingADPostfixPOPEnabled', 'msExchHideFromAddressLists', 'hostingADPostfixForwardingAddresses', 'hostingADPostfixForwardingAddresses', 'hostingADPostfixTotalItemSize', 'hostingADPostfixTotalItemCount', 'lastLogonTimestamp', 'whenCreated', 'whenChanged', 'hostingMailfilterNextHop')

    #Get LDAP user list
    ldap_user_list=get_ldap_user_list()

    dict_with_all_users={}


    for i in ldap_user_list:
        # Prepare searchFilter. Users are getting with the following format:
        # cn: Abigail.Lyons@easyJet but we need only Abigail.Lyons@easyJet
        searchFilter="CN"+"="+i[4:]
        logging.info(i[4:])
        #Getting ldap data
        ldap_result = l.search(baseDN, searchScope, searchFilter, list(retrieveAttributes))
        result_set=[]
        result_set_new=[]

        while 1:
            result_type, result_data = l.result(ldap_result, 0)
            if (result_data == []):
                break
            else:
                if result_type == ldap.RES_SEARCH_ENTRY:
                    result_set.append(result_data)
        try:
            result_set_new=result_set[0]
            result_set=result_set_new[0]
            result_set_new=result_set[1]
            username=result_set[0].split(',')[0]
        except IndexError:
            logging.info("Exception")
            continue

        total_val={}


        for key,value in result_set_new.items():  # Convert some timestamps to Human readable
            value=' '.join(value)
            if key == 'lastLogonTimestamp':
                value=lastLogonTimestamp_converter(value)
            elif key == 'whenCreated' or key == 'whenChanged':
                value=converter2(value)
            elif key == 'hostingMailfilterNextHop':
                value=value[5:]
            total_val[key]=value

        list_of_dict_values=[]
        for item in retrieveAttributes: # Some users has no some attributes in LDAP.
                                        # Making those attributes value 'None'
            if item in total_val.keys():
                list_of_dict_values.append(total_val[item])
            else:
                list_of_dict_values.append('None')
        last_dict={}
        last_dict[i[4:]]=list_of_dict_values
        dict_with_all_users.update(last_dict)

    report_generate(dict_with_all_users)

def get_ldap_user_list():
    logging.info("Getting ldap users")
    try:
        os.system('ldapsearch -Hldap://ldap.exch500.serverdata.net -b "OU=easyJet,OU=Hosting,DC=exch500,DC=msoutlookonline,DC=net" "(&(objectClass=user)(objectCategory=person)(hostingObjectType=ADPostfixMailbox))" cn -x -w vgy7gr39juhaejawe5hg534y45tgw45f -D "ADPostfixLDAPSvc@exch500.msoutlookonline.net" | grep ^cn: | awk "{print $2}" > /var/tmp/users')
        temp=open("/var/tmp/users", "r")
        ldap_user_list = temp.read().splitlines()
    except IOError:
        logging.info("Couldn't execute ldapsearch command and get user list")
    return ldap_user_list

def lastLogonTimestamp_converter(value):
    time=datetime.fromtimestamp((int(value)/10000000) - (((1970 - 1601) * 365 - 3 + round((1970 - 1601) / 4)) * 86400)).strftime('%Y-%m-%d %H:%M:%S')
    return(time)

def converter2(value):
    time=value[:4]+'-'+value[4:6]+'-'+value[6:8]+' '+value[8:10]+':'+value[10:12]+':'+value[12:14]
    return(time)

def report_generate(value):
    w = csv.writer(open(REPORT_F, "w"))
    for key, val in value.items():
        logging.info(val)
        w.writerow([str(val).replace('"',"'").replace("[","").replace("]","").replace("', '","|").replace("'", "")])

if __name__ == "__main__":
    main()
