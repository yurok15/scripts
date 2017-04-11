#!/usr/bin/python2.7
###########################################################
#
# This python script is used for restore IMAP from backup
#
#
# Written by : Yuriy Zhigulskiy
# Created date: Apr 05, 2017
# Last modified: Apr 05, 2017
# Tested with : Python 2.7.6
# Script Revision: 0.1
#
##########################################################

import os
import shutil
from stat import *

SOURCE_DIRECTORY="/var/tmp/FP2561961"
DEST_DIRECTORY="/tmp/imedia/users/testaccount/mailbox1"
RESTORE_DATE=".restore_05_04_2017"

def main():
    dest_dir=(DEST_DIRECTORY+"/"+RESTORE_DATE)
    os.mkdir(dest_dir)
    if check_directory_exist(SOURCE_DIRECTORY, DEST_DIRECTORY) is True:
        list=os.listdir(SOURCE_DIRECTORY)
        copy(list)
    else:
        print("SOURCE or DESTINATION directory doesnt exist")

def copy(list):
    for i in list:
        source_dir=str(SOURCE_DIRECTORY+"/"+i)
        mode=os.stat(source_dir).st_mode
        if S_ISDIR(mode):  # check source_dir is a directory
            if i.startswith("."):
                # copy to special DEST_DIRECTORY
                dest_dir=DEST_DIRECTORY+"/"+RESTORE_DATE+"."+i[1:]
                shutil.copytree(source_dir, dest_dir)
            else:
                dest_dir=DEST_DIRECTORY+"/"+RESTORE_DATE+"/"+i
                shutil.copytree(source_dir, dest_dir)
        else:  # if source_dir is a file
            dest_dir=DEST_DIRECTORY+"/"+RESTORE_DATE+"/"+i
            shutil.copyfile(source_dir, dest_dir)

def check_directory_exist(SOURCE_DIRECTORY, DEST_DIRECTORY):
    a=os.path.exists(SOURCE_DIRECTORY)
    b=os.path.exists(DEST_DIRECTORY)
    if a and b is True:
        return(True)
    else:
        return(False)

if __name__ == "__main__":
    main()
