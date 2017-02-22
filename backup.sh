#!/bin/bash

################################################################################
## Compression level: 1 - fast, 3,4 -optimal, 6 - slow,but stronger
##
# This param should be setupped

NOTIFICATION_ADDRESS=
backuproot=""


COMPRESSION="3"
################################################################################

export FAILED=0
export SUCCESS=0
export TOTAL=0

timestamp=`date "+%Y-%m-%d-%H-%M-%S"`
hostname=`/bin/hostname`

logs="/var/log/backup"
mkdir -p ${logs}

logfile="${logs}/backup-${timestamp}.log"

temproot="/var/lib/backup"
tempdir="${temproot}/${timestamp}"
report='/tmp/mysqlbackups.lst'

mkdir -p ${tempdir}

if mount | grep $backuproot > /dev/null; then
    while ( umount ${backuproot} 1>/dev/null 2>&1 ); do echo "Unmounting  backup dir" >> ${logfile}; sleep 1; done
fi


echo "Backup task started: `date "+%Y-%m-%d-%H-%M-%S"`" >> ${logfile}
echo "Mounting ${backuproot}" >> ${logfile}
    mount ${backuproot}
    RETVAL=$?
    if [ $RETVAL -ne 0 ]; then
        echo "Cannot mount ${backuproot}" >> ${logfile}
        umount ${backuproot} || umount -l ${backuproot}
        echo "Can't mount backup share. Please check." | mail -s "Backup of `hostname` failed" $NOTIFICATION_ADDRESS
        exit $RETVAL
    fi

echo "Creating network backupdir" >> ${logfile}
    backupdir="${backuproot}/${hostname}/${timestamp}"
    echo "backupdir=${backupdir}" >> ${logfile}
    mkdir -p ${backupdir}
    RETVAL=$?
    if [ $RETVAL -ne 0 ]; then
        echo "Cannot mkdir ${backupdir}" >> ${logfile}
        echo "Can't create backup dir. Please check." | mail -s "Backup of `hostname` failed" $NOTIFICATION_ADDRESS
        umount ${backuproot} || ( umount -l ${backuproot} || exit 253 )
        exit $RETVAL
    fi

echo "Backing up /etc" >> ${logfile}
    ctimestamp=`date "+%Y-%m-%d-%H-%M-%S"`
    command="tar -czf ${backupdir}/etc-${ctimestamp}.tar.gz /etc"
    echo "${ctimestamp}: Executing: ${command}" >> ${logfile}
    eval ${command} >> ${logfile} 2>&1

# Databases list
#dblist=`mysql --user=local_backup --password= -e 'SHOW DATABASES' | egrep -iv 'Database|information_schema'`

#declare -a BACKUP
#declare -i index

#index=1
#for database in $dblist
mysql --user=local_backup --password= -e 'SHOW DATABASES' | egrep -iv '^information_schema$' | while read database
do
    export TOTAL=$(($TOTAL+1))
    ctimestamp=`date "+%Y-%m-%d-%H-%M-%S"`
# Fix for "?" in database names
    fdatabase=`echo $database| sed 's/?/_/' | sed 's/ /_/'`
    
    echo "${ctimestamp}: backing up $database to temporary dir ${tempdir}" >> ${logfile}

#    command="mysqldump -u local_backup --password= --force \"$database\" --lock-tables --add-drop-table > ${backupdir}/$fdatabase-${ctimestamp}.sql"
    command="mysqldump -u local_backup --password= --force \"$database\" --lock-tables --add-drop-table > ${tempdir}/$fdatabase-${ctimestamp}.sql"

    echo "Backing up ${database}" >> ${logfile} 2>&1
    echo "Command: $command" >> ${logfile}
    eval $command >> ${logfile} 2>&1
    
    RETVAL=$?
    if [ $RETVAL -ne 0 ]; then
    		echo "WARNING: ${command} exited with non-zero status ${RETVAL}" >> ${logfile}
		export FAILED=$(($FAILED+1))
    else
		export SUCCESS=$(($SUCCESS+1))
    fi
#    [ -f ${backupdir}/$fdatabase-${ctimestamp}.sql ] && gzip -$COMPRESSION ${backupdir}/$fdatabase-${ctimestamp}.sql
     [ -f ${tempdir}/$fdatabase-${ctimestamp}.sql ] && gzip -$COMPRESSION ${tempdir}/$fdatabase-${ctimestamp}.sql
#    index=index+1
done

if [ $SUCCESS -lt $TOTAL ]; then
        echo "Only $SUCCESS of $TOTAL databases was successfully archived. $FAILED failed. Please check." | mail -s "Backup of `hostname` failed" $NOTIFICATION_ADDRESS
else
	echo "Created backup for $SUCCESS of $TOTAL databases." >> ${logfile}
        touch ${backupdir}/SUCCESS
fi

#copy from localdisk to network location
    echo "Copying from tempdir to network backup location: `date "+%Y-%m-%d-%H-%M-%S"`" >> ${logfile}
    command="cp -v ${tempdir}/* ${backupdir}/"
    echo "Command: ${command}" >> ${logfile} 2>&1
    eval $command >> ${logfile} 2>&1
    RETVAL=$?
    if [ $RETVAL -ne 0 ]; then
    		echo "WARNING: ${command} exited with non-zero status ${RETVAL}" >> ${logfile}
		export FAILED=$(($FAILED+1))
    else
		export SUCCESS=$(($SUCCESS+1))
    fi
    echo "Copied from tempdir to network backup location: `date "+%Y-%m-%d-%H-%M-%S"`" >> ${logfile}

#backupclean
    command="/usr/bin/find ${backuproot}/${hostname}/ -maxdepth 1 -type d -ctime +15 -print | xargs rm -rvf "
    echo $command >> ${logfile}
    eval $command >> ${logfile} 2>&1
    RETVAL=$?
    if [ $RETVAL -ne 0 ]; then
            echo "WARNING: '$command' returned non-zero status ${RETVAL}" >> ${logfile}
    fi

#tempdir clean
    command="/usr/bin/find ${temproot}/ -maxdepth 1 -type d -ctime +3 -print | xargs rm -rvf "
    echo $command >> ${logfile}
    eval $command >> ${logfile} 2>&1
    RETVAL=$?
    if [ $RETVAL -ne 0 ]; then
            echo "WARNING: '$command' returned non-zero status ${RETVAL}" >> ${logfile}
    fi

#Unmount
    echo "Unmounting ${backuproot}" >> ${logfile}
    umount -l ${backuproot} 1>/dev/null 2>&1
    RETVAL=$?
    if [ $RETVAL -ne 0 ]; then
        echo "Cannot unmount ${backuproot}" >> ${logfile}
        exit $RETVAL
    fi
    
echo $FAILED>>$report
echo "Backup task finished: `date "+%Y-%m-%d-%H-%M-%S"`" >> ${logfile}
