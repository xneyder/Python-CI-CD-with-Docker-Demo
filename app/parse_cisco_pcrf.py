#!/usr/bin/python
# parse_cisco_pcrf.py

#
# Description: Demo for CI/CD
#       This process runs on the background constanly checking the
#       input dirs for new raw data files, then it parses the file and loads it
#       to the mysql table CISCO_PCRF_CPU
#
# Input Format Example:
#    NE_NAME,CPU_ID,STEAL,IDLE,CPU_USER,SYSTEM,WAIT
#   lab2-sm04,1,0,805913474,16055345,13320893,11593
#   lab2-sm04,0,0,806140814,15821592,13445785,7637
#   lab2-ps04,8,0,246496014,1997551,1407157,2402
#   lab2-ps04,9,0,246038999,2239524,1484897,1861
#   lab2-sm04,5,0,805460474,16089293,13884955,8350
#
# Input Parameters:
#       INPUT_FOLDER: The input raw data folder
#
# Example:
#       parse_cisco_pcrf.py "/raw_data/inputs/"
#
# Database: MYSQL
#
# Created by : Daniel Jaramillo
# Creation Date: 20/11/2018
# Modified by:     Date:
# All rights(C) reserved to Teoco
###########################################################################

import sys

import mysql.connector
import glob
import os
import base64
import time
import pandas as pd
from LoggerInit import LoggerInit
from datetime import datetime

####
#Description: creates a mysql connection
#output: mysql db object
def get_mysql_connection():
    app_logger=logger.get_logger("get_mysql_connection")
    #Get env variables
    try:
        db_host=os.environ['DB_HOST']
        db_user=os.environ['DB_USER']
        db_password=os.environ['DB_PASSWORD']
        db_name=os.environ['DB_NAME']
    except KeyError as err:
        app_logger.error(err)
        raise Exception(err)
    #Define Database Connection
    try:
        db = mysql.connector.connect(
            host=db_host,
            user=db_user,
            passwd=base64.b64decode(db_password),
            database=db_name
        )
    except mysql.connector.Error as err:
        app_logger.error(err)
        raise Exception(err)
    return db

####
#Description: parses and loads the file to the database
#input: file name
def load_file(filename):
    global logger
    #Define Database Connection
    db=get_mysql_connection()
    cursor = db.cursor()
    app_logger=logger.get_logger("load_file")
    pmm_datetime=datetime.strptime(filename.split('-')[-2],'%Y%m%d%H%M')
    df=pd.read_csv(filename)
    sql = """INSERT INTO CISCO_PCRF_CPU (PMM_DATETIME, NE_NAME, CPU_ID, STEAL,
        IDLE, CPU_USER, _SYSTEM, WAIT) VALUES ('{pmm_datetime}', 
        %s, %s, %s, %s, %s, %s, %s)""".format(pmm_datetime=pmm_datetime)
    try:
        cursor.executemany(sql, df.values.tolist())
        db.commit()
    except mysql.connector.Error as err:
        app_logger.error(err)
        raise Exception(err)
    app_logger.info('{rowcount} records were inserted to table CISCO_PCRF_CPU.'
                    .format(rowcount=cursor.rowcount))
    return True


#Main function
def main():
    sleep_time=10
    app_logger=logger.get_logger("main")
    app_logger.info("Starting {script}".format(script=sys.argv[0]))
    #Validate the line arguments
    if len(sys.argv) < 2:
        app_logger.error("Usage {script} 'input folder'"
                         .format(script=sys.argv[0]))
        app_logger.error("Example {script} '/raw_data/inputs/'"
                         .format(script=sys.argv[0]))
        raise Exception("Example {script} '/raw_data/inputs/'"
                         .format(script=sys.argv[0]))
    #check if input_folder exists
    input_folder=sys.argv[1]
    if not os.path.isdir(input_folder):
        app_logger.error("Folder {input_folder} does not exist"
                         .format(input_folder=input_folder))
        raise Exception("Folder {input_folder} does not exist"
                         .format(input_folder=input_folder))
    #look for all files in an infinite loop
    while True:
        file_list=glob.glob(os.path.join(input_folder,"*csv"))
        #sleep to make sure all files are closed
        app_logger.info("Sleeping {sleep_time} seconds"
                        .format(sleep_time=sleep_time))
        time.sleep(sleep_time)
        for filename in file_list:
            load_file(filename)
            #os.rename(filename,filename+"_")



#If LOG_DIR environment var is not defined use /tmp as logdir
if 'LOG_DIR' in os.environ:
    log_dir=os.environ['LOG_DIR']
else:
    log_dir="/tmp"
#Define logger
log_file=os.path.join(log_dir,sys.argv[0])
logger=LoggerInit(log_file,10)

#Application starts here
if __name__ == "__main__":
    main()

