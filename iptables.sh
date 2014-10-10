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

ALLOURNETS=" "

SPBOFFICE=" "

PAOFFICE=" "

SYSLOGNET=" " 

HOSTINGNET=""

NTPSERVERS=" "
SLOGSERVERS=" "

SNMPBOXES=" "

DNSSERVERS=""

SPAMMERS=`cat /etc/network/spammers`

HEARTBEATNET=" "

WEHOSTS=" "
TASKSC=""
SSLPROXY=" "

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
