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
import sys, getopt
from datetime import datetime

#CURRENT_DATE=datetime.now().strftime("%y-%m-%d-%H-%M-%S")
from stat import *


#SOURCE_DIRECTORY="/var/tmp/FP2561961"
#DEST_DIRECTORY="/tmp/imedia/users/testaccount/mailbox1"
global SOURCE_DIRECTORY
SOURCE_DIRECTORY=""
global DEST_DIRECTORY
DEST_DIRECTORY=""
RESTORE_DATE=".restore"+"_"+datetime.now().strftime("%d_%m_%Y")

def main(argv):
    SOURCE_DIRECTORY, DEST_DIRECTORY = check_arguments(argv)
    dest_dir=(DEST_DIRECTORY+"/"+RESTORE_DATE)
    os.mkdir(dest_dir)

    if check_directory_exist(SOURCE_DIRECTORY, DEST_DIRECTORY) is True:
        list=os.listdir(SOURCE_DIRECTORY)
        copy(list, SOURCE_DIRECTORY, DEST_DIRECTORY)
    else:
        print("SOURCE or DESTINATION directory doesnt exist")

def copy(list, SOURCE_DIRECTORY, DEST_DIRECTORY):
    for i in list:
        source_dir=str(SOURCE_DIRECTORY+"/"+i)
        print
        print(source_dir)
        mode=os.stat(source_dir).st_mode
        if S_ISDIR(mode):  # check source_dir is a directory
            if i.startswith("."):
                dest_dir=DEST_DIRECTORY+"/"+RESTORE_DATE+"."+i[1:]
                shutil.copytree(source_dir, dest_dir)
            else:
                dest_dir=DEST_DIRECTORY+"/"+RESTORE_DATE+"/"+i
                shutil.copytree(source_dir, dest_dir)
        else:  # if source_dir is a file
            dest_dir=DEST_DIRECTORY+"/"+RESTORE_DATE+"/"+i
            shutil.copyfile(source_dir, dest_dir)

def check_arguments(argv):
    myopts, args = getopt.getopt(sys.argv[1:],"s:d:h")
    for o, a in myopts:
        if o == '-h':
            print("Usage: %s -s /source -d /destination" % sys.argv[0])
        elif o == '-s':
            SOURCE_DIRECTORY=a
        elif o == '-d':
            DEST_DIRECTORY=a
        else:
            print("Usage: %s -s input -d output" % sys.argv[0])
    #print ("Input file : %s and output file: %s" % (SOURCE_DIRECTORY,DEST_DIRECTORY) )
    return(SOURCE_DIRECTORY, DEST_DIRECTORY)

def check_directory_exist(SOURCE_DIRECTORY, DEST_DIRECTORY):
    a=os.path.exists(SOURCE_DIRECTORY)
    b=os.path.exists(DEST_DIRECTORY)
    if a and b is True:
        return(True)
    else:
        return(False)

if __name__ == "__main__":
    main(sys.argv[1:])
