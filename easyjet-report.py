import ldap.modlist as modlist
import time
import datetime
import os
from datetime import datetime
import csv
import os
import ldap

REPORT_FILE="easyjet-report"
REPORT_F="/var/tmp/easyjet_report"+"_"+datetime.now().strftime("%d_%m_%Y")
user_list = []

l = ldap.initialize("ldap://ldap.exch500.serverdata.net:389/")
l.simple_bind_s("ADPostfixLDAPSvc@exch500.msoutlookonline.net", "vgy7gr39juhaejawe5hg534y45tgw45f")
baseDN = "OU=easyJet,OU=Hosting,DC=exch500,DC=msoutlookonline,DC=net"
searchScope = ldap.SCOPE_SUBTREE
retrieveAttributes=('displayName', 'cn', 'targetAddress', 'hostingADPostfixPOPEnabled', 'msExchHideFromAddressLists', 'hostingADPostfixForwardingAddresses', 'hostingADPostfixForwardingAddresses', 'hostingADPostfixTotalItemSize', 'hostingADPostfixTotalItemCount', 'lastLogonTimestamp', 'whenCreated', 'whenChanged')


#convert LDAP timestamp to Human readable
def lastLogonTimestamp_converter(value):
    #print(value)
    time=datetime.fromtimestamp((int(value)/10000000) - (((1970 - 1601) * 365 - 3 + round((1970 - 1601) / 4)) * 86400)).strftime('%Y-%m-%d %H:%M:%S')
    #print(time)
    return(time)
def converter2(value):
    time=value[:4]+'-'+value[4:6]+'-'+value[6:8]+' '+value[8:10]+':'+value[10:12]+':'+value[12:14]
    return(time)
def report_generate(value):
#fd=open(REPORT_F, "w")
    w = csv.writer(open(REPORT_F, "w"))
    for key, val in value.items():
        #w.writerow([val])
        w.writerow([str(val).replace("[","").replace("]","").replace("', '","|").replace("'", "")])

#os.system('ldapsearch -Hldap://ldap.exch500.serverdata.net -b "OU=easyJet,OU=Hosting,DC=exch500,DC=msoutlookonline,DC=net" "(&(objectClass=user)(objectCategory=person)(hostingObjectType=ADPostfixMailbox))" cn -x -w vgy7gr39juhaejawe5hg534y45tgw45f -D "ADPostfixLDAPSvc@exch500.msoutlookonline.net" | grep ^cn: | awk "{print $2}" > /var/tmp/users')
temp=open("/var/tmp/users", "r")
file = temp.read().splitlines()
new_result_set={}
dict_with_all_users={}
for i in file:
    searchFilter="CN"+"="+i[4:]
    #searchFilter=i
    #print(searchFilter)
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




#result_set=[[('CN=Flavien.Rousseau@easyJet,OU=easyJet,OU=Hosting,DC=exch500,DC=msoutlookonline,DC=net', {'displayName': ['Flavien Rousseau (ORY)'], 'hostingADPostfixTotalItemCount': ['3683'], 'hostingADPostfixTotalItemSize': ['900'], 'whenChanged': ['20170420121433.0Z'], 'targetAddress': ['SMTP:Flavien.Rousseau@easyJet.com'], 'lastLogonTimestamp': ['131364829401409656'], 'whenCreated': ['20120606025120.0Z'], 'hostingADPostfixIMAPEnabled': ['TRUE']})]]

    result_set_new=result_set[0]

    result_set=result_set_new[0]
    result_set_new=result_set[1]
    #print(result_set_new)
    username=result_set[0].split(',')[0]
    #print(username)
    #dict_with_all_users={}
    total_val={}

    for key,value in result_set_new.items():
        value=' '.join(value)
        if key == 'targetAddress':
            value=value
        elif key == 'lastLogonTimestamp':
            value=lastLogonTimestamp_converter(value)
        elif key == 'whenCreated' or key == 'whenChanged':
        #elif key ==
            value=converter2(value)
        total_val[key]=value
        #total_val.append(value)
    #print(total_val)

    list_of_dict_values=[]
    for item in retrieveAttributes:
        if item in total_val.keys():
            list_of_dict_values.append(total_val[item])
        else:
            list_of_dict_values.append('None')
    last_dict={}
    last_dict[i[4:]]=list_of_dict_values

    dict_with_all_users.update(last_dict)



#print("record to file")
report_generate(dict_with_all_users)






   #list1=[]
    #username=i[4:]
    #print(result_set_new)
    #for item in retrieveAttributes:
    #    if item in result_set_new.keys():
    #        list1.append(result_set_new[item])
    #    else:
    #        list1.append('None')
    #print(list1)
    #new_result_set[username] = list1


    #print(result_set_new)
    #retrieveAttributes=('cn', 'targetAddress', 'hostingADPostfixIMAPEnabled', 'displayName', 'msExchHideFromAddressLists', 'hostingADPostfixForwardingAddresses', 'hostingADPostfixTotalItemSize', 'hostingADPostfixTotalItemCount', 'lastLogonTimestamp', 'whenCreated', 'whenChanged', 'lastLogonTimestamp')
    #print(result_set_new)
    #dict_last={}


    #for item in retrieveAttributes:
        #print('test')
        #print(item)
    #    if item in result_set_new.keys():
    #        dict_last[item]=result_set_new[item]
    #    else:
    #        dict_last[item]='None'
    #print('test')
    #print(dict_last)
