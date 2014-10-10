#!/bin/bash

IPT="/sbin/iptables"

################################################################################
#
# Use /etc/network/ipt-custom.inc to add custom "per box" rules
# this file will be included if exists later in script.
#
################################################################################

################################################################################
# Some variables
################################################################################

ALL="0.0.0.0/0"

ALLOURNETS="206.40.48.0/24 207.5.0.0/17 64.78.0.0/18 10.254.0.0/16 10.10.192.0/24 10.240.0.0/16 10.16.182.0/24 172.16.0.0/12 "

SPBOFFICE="10.9.0.0/22 10.5.5.0/24 "

PAOFFICE="10.16.183.0/24 "

SYSLOGNET="64.78.0.0/16 207.5.0.0/16 10.254.0.0/16 " 

HOSTINGNET="206.40.48.0/24 64.78.61.0/24 10.254.244.0/24"

NTPSERVERS="64.78.61.247 207.5.44.4 "
SLOGSERVERS="64.78.18.243 64.78.61.249 "

SNMPBOXES="207.5.44.10 207.5.44.11 207.5.44.12 64.78.19.204 207.5.74.137 207.5.74.138 10.254.254.27 10.240.128.15 10.254.254.64 10.200.8.10 64.78.59.245 10.240.254.223 172.30.31.23 10.240.128.65 10.216.233.16 10.216.233.17 10.224.233.16 10.224.233.17 10.250.0.5 10.92.23.24 10.92.23.25 10.36.156.24 10.36.156.25 10.32.4.105 10.249.32.116 "

DNSSERVERS="207.5.44.4 64.78.61.247"

SPAMMERS=`cat /etc/network/spammers`

HEARTBEATNET="239.0.0.0/8 64.78.0.0/18 207.5.72.0/22 "

WEHOSTS="10.254.244.0/24 10.240.168.0/24 10.254.252.0/24 10.240.166.0/24 10.240.254.223 10.254.156.0/24 10.240.156.0/24 172.30.31.120 "
TASKSC="10.254.240.0/24 10.254.254.82"
SSLPROXY="207.5.73.4 207.5.73.5 "

################################################################################
# Some subroutines
################################################################################

setDefaultPolicy() {
$IPT -P $1 $2
}

allowEverything() {
$IPT -A INPUT -s $1 -j ACCEPT
}

allowTcpPortInput() {
$IPT -A INPUT -s $1 -p tcp --dport $2 -j ACCEPT
}

denyTcpPortInput() {
$IPT -A INPUT -s $1 -p tcp --dport $2 -j REJECT
}


allowIcmp() {
$IPT -A INPUT -p icmp -s $1 -j ACCEPT
}

allowUdpPortInput() {
$IPT -A INPUT -s $1 -p udp -m udp --dport $2 -j ACCEPT
}

commonNetSetup() {

$IPT -A INPUT -i lo -j ACCEPT
$IPT -A INPUT -p esp -j ACCEPT
$IPT -A INPUT -p ah -j ACCEPT
$IPT -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT

}


clearRules() {
#Clear all rules
$IPT -F
$IPT -X

}

################################################################################
# Initial defaults

#Clear all rules first
clearRules

#Common network setup
commonNetSetup

#Drop all incoming traffic by default
setDefaultPolicy "INPUT" "DROP"

# Allow rppcd to WEHOSTS TASKSC and SSLPROXY
for net in $WEHOSTS $TASKSC $SSLPROXY
do
allowTcpPortInput $net 3333
done
# Deny for all the rest
denyTcpPortInput 0.0.0.0/0 3333

################################################################################                            
# Custom part                                                                                               
################################################################################                            
if [ -f /etc/network/ipt-custom.inc ]; then source /etc/network/ipt-custom.inc; fi
################################################################################               




#Allow everything from Offices
for net in $SPBOFFICE $PAOFFICE $DNSSERVERS
do
allowEverything  $net
done

#Allow SSH from our networks, offices and homes. And syslogs.
for net in $ALLOURNETS $SPBOFFICE $SLOGSERVERS
do
allowTcpPortInput $net 22
done

#Allow SYSLOG for linux hosting
for net in $SYSLOGNET
do
allowUdpPortInput $net 514
done

#Block spammers
for net in $SPAMMERS
do
denyTcpPortInput $net 25
done

#Allow Public SMTP
for net in $ALL
do
allowTcpPortInput $net 25
allowTcpPortInput $net 2501
done

#Allow icmp
for net in $ALL
do
allowIcmp $net
done

#Allow mysql
for net in $ALLOURNETS
do
allowTcpPortInput $net 3306
done

#Allow snmp
for net in $SYSLOGNET $SNMPBOXES
do
allowUdpPortInput $net 161
done

#Allow heartbeat
for net in $HEARTBEATNET
do
allowUdpPortInput $net 694
done

#Allow DNS for monitoring
for net in $ALLOURNETS
do
allowUdpPortInput $net 53
allowTcpPortInput $net 53
done

#Allow CTASD for monitoring
for net in $ALLOURNETS $SNMPBOXES
do
allowTcpPortInput $net 8088
done
