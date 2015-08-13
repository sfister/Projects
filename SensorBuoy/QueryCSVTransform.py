import pymssql
import time
import datetime
import os.path
import traceback
import csv


""" This scritp will connect to the sensorbuoy database and extract the Wave data from the database.
This wave data will then be saved in a time stamped file.
There is a control file that is used to set how far back in time to select data from the database.
This file is simply a timestamp.
If you need to re-run or re-extract hitorical data from the source database adjust the timestampfile to the time
you want to start extracting data from the tables.
"""

class QueryCSVTransform(object):
    def __init__(self, controlfile, outputpath, dbhost, dbuser, dbpassword, dbname, queryString, fileprefix, **kwargs):
        self.controlfile = controlfile
        self.outputpath = outputpath
        self.dbhost = dbhost
        self.dbuser = dbuser
        self.dbpassword = dbpassword
        self.dbname = dbname
        self.queryString = queryString
        self.fileprefix = fileprefix
        
    def run(self):

        cnxn = pymssql.connect(host=self.dbhost, user=self.dbuser, password=self.dbpassword, \
                               database=self.dbname, as_dict=True)

        st = datetime.datetime.utcnow().strftime('%Y%m%d%H%M')

        if os.path.isfile(self.controlfile):
            cntlFile = open(self.controlfile, "r+")
            startTime = cntlFile.readline()
            startTime = startTime.strip()
        else:
            startTime = '2000-01-01 00:00:00'
            cntlFile = open(self.controlfile, "w+")

        sqlQuery = self.queryString.format(startTime)

        cursor = cnxn.cursor()

        outputFileName = "{0}{1}_{2}.txt".format(self.outputpath,self.fileprefix,st)

        cursor.execute(sqlQuery)
        rows = cursor.fetchall()
        finalTimeStamp = ''

        fieldnames= []
        for cntr in range(len(cursor.description)):
            fieldnames.append(cursor.description[cntr][0])

        with open(outputFileName, 'w+') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
                finalTimeStamp = row["DataTimeStamp"]

        if finalTimeStamp:
            cntlFile.seek(0)
            cntlFile.truncate()
            cntlFile.write(str(finalTimeStamp))
            cntlFile.write("\n")
            cntlFile.close


class QueryCSVTransform2Stage(object):
    def __init__(self, controlfile, outputpath, dbhost, dbuser, dbpassword, dbname, queryString1, \
                 queryString2, fileprefix, **kwargs):
        self.controlfile = controlfile
        self.outputpath = outputpath
        self.dbhost = dbhost
        self.dbuser = dbuser
        self.dbpassword = dbpassword
        self.dbname = dbname
        self.queryString1 = queryString1
        self.queryString2 = queryString2
        self.fileprefix = fileprefix


    def run(self):
        finalTimeStamp = ''
        try:

            cnxn = pymssql.connect(host=self.dbhost, user=self.dbuser, password=self.dbpassword, \
                            database=self.dbname, as_dict=True)

            #First we need to get the last reference date when the process last ran.
            st = datetime.datetime.utcnow().strftime('%Y%m%d%H%M')

            if os.path.isfile(self.controlfile):
                cntlFile = open(self.controlfile, "r+")
                startTime = cntlFile.read()
                if startTime == None:
                    startTime = '2000-01-01 00:00:00'
                startTime = startTime.replace("\n", "")
            else:
                startTime = '2000-01-01 00:00:00'
                cntlFile = open(self.controlfile, "w")

            #First lets get the unique ids that need to be fetched base on the last time we processed the data.
            sqlQueryInitial = self.queryString1.format(startTime)

            cursor = cnxn.cursor()
            cursor.execute(sqlQueryInitial)
            fileSets = cursor.fetchone()

            outputFileName = "{0}{1}_{2}.txt".format(self.outputpath, self.fileprefix, st)
            outputFile = open(outputFileName, "w")

            #Now we need to get the Column list to pivot the rows into.
            sqlQueryStuff = self.queryString2.format(startTime, fileSets["sqlString"].replace('.','_').strip())

            cursorStuff = cnxn.cursor()
            cursorStuff.execute(sqlQueryStuff)

            fieldnames= []
            for cntr in range(len(cursorStuff.description)):
                fieldnames.append(cursorStuff.description[cntr][0])

            with open(outputFileName, 'w+') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in cursorStuff.fetchall():
                    writer.writerow(row)
                    finalTimeStamp = row["DataTimeStamp"]

                cursorStuff.close()

            cursor.close()

        except Exception, err:
            print(traceback.format_exc())
        finally:
            cnxn.close()

            if finalTimeStamp:
                cntlFile.seek(0)
                cntlFile.truncate()
                cntlFile.write(str(finalTimeStamp))
                cntlFile.write("\n")
                cntlFile.close

