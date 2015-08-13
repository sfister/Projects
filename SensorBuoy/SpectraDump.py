import pyodbc
import time
import datetime
import os.path

timestampfile = "C:/SensorBouy/SensorControl/SpectraDateFile.txt"
outputPath= "C:/SensorBouy/SensorDump/"
cnxn = pyodbc.connect('DSN=AXYSDMS;UID=sa;PWD=syxaV8L5X2')
finalTimeStamp = ''

try:

	#First we need to get the last reference date when the process last ran.
	st = datetime.datetime.utcnow().strftime('%Y%m%d%H%M')

	if os.path.isfile(timestampfile):
		cntlFile = open(timestampfile, "r+")
		startTime = cntlFile.read()
		if startTime == None:
			startTime = '2000-01-01 00:00:00'
		startTime = startTime.replace("\n", "")
	else:
		startTime = '2000-01-01 00:00:00'
		cntlFile = open(timestampfile, "w")

	outputFile = None
	cursorData = None
	fileSet = None
	
	#First lets get the unique ids that need to be fetched base on the last time we processed the data.
	sqlQueryInitial = "select top 100 [TRIAXYSDirectionalSpectraHeaderDBID] as DBID \
		      ,[Version] \
		      ,[TASSerialNumber] \
		      ,[BuoyID]\
		      ,[Location]\
		      ,[NumberOfFrequencies]\
		      ,[NumberOfDirections]\
		      ,[InitialFrequency]\
		      ,round([D_Frequency], 4) as [D_Frequency]\
		      ,[D_Theta]\
		      ,round([ResolvableFrequencyRangeStart], 4) as [ResolvableFrequencyRangeStart]\
		      ,round([ResolvableFrequencyRangeEnd], 4) as [ResolvableFrequencyRangeEnd]\
		      , replace(replace(replace(convert(varchar(17), DataTimeStamp, 120),'-',''), ':',''), ' ', '') as dateTime \
		      , DataTimeStamp \
	         from [axDMSPluginTRIAXYSDirectionalSpectraHeader] \
			 where DataTimeStamp > '{0}' order by DataTimeStamp asc;".format(startTime)

	cursor = cnxn.cursor()
	cursor.execute(sqlQueryInitial)
 	for fileSet in cursor.fetchall():
		outputFileName = "{0}Spectra_{1}.txt".format(outputPath,fileSet.dateTime)
		outputFile = open(outputFileName, "w")

		#Now we need to get the Column list to pivot the rows into.
		sqlQueryStuff = "select stuff((select distinct ',' + QUOTENAME(right(replicate('0', 2) + convert(varchar, direction), 5)) \
		 from [axDMSPluginTRIAXYSDirectionalSpectraDetails] \
		 where TRIAXYSDirectionalSpectraHeaderDBID = '{0}' \
		 and Frequency = 0 \
		  for XML path(''), type).value('.', 'NVARCHAR(MAX)'), 1, 1, '');".format(fileSet.DBID)

		outputFile.write("TRIAXYS BUOY REPORT - "+fileSet.TASSerialNumber+" - \n")
		outputFile.write("VERSION   = "+fileSet.Version+'\n')
		outputFile.write("TYPE      = DIRECTIONAL SPECTRUM\n")
		outputFile.write("DATE      = "+str(fileSet.DataTimeStamp)+"(UTC)\n")
		outputFile.write("NUMBER OF FREQUENCIES              = "+str(fileSet.NumberOfFrequencies)+"\n")
		outputFile.write("INITIAL FREQUENCY (Hz)             = "+str(fileSet.InitialFrequency)+"\n")
		outputFile.write("FREQUENCY SPACING (Hz)             = "+str(fileSet.D_Frequency)+"\n")
		outputFile.write("RESOLVABLE FREQUENCY RANGE (Hz)    = "+str(fileSet.ResolvableFrequencyRangeStart)\
			+" TO  "+str(fileSet.ResolvableFrequencyRangeEnd)+"\n")
		outputFile.write("NUMBER OF DIRECTIONS               =  "+str(fileSet.NumberOfDirections)+"\n")
		outputFile.write("DIRECTION SPACING (DEG)            =  "+str(fileSet.D_Theta)+"\n")
		outputFile.write("COLUMNS = 0.00 TO 360.00 DEG\n")
		outputFile.write("ROWS	= 0.00 TO   0.64 Hz\n")

		cursorStuff = cnxn.cursor()
		cursorStuff.execute(sqlQueryStuff)
		colList = ""
		for stuffList in cursorStuff.fetchall():
			colList = stuffList[0]
			break;
		cursorStuff.close()

		if colList:
			#now we need to actually get the data for the file.
			sqlQuery = "select * \
			  from (select Frequency, Direction, Energy \
			   from [axDMSPluginTRIAXYSDirectionalSpectraDetails] as sd \
			   where TRIAXYSDirectionalSpectraHeaderDBID in ('{0}') \
			 ) as t \
			 pivot ( max(Energy)\
			 for Direction in ({1})) as p ;".format(fileSet.DBID, colList)
			cursorData = cnxn.cursor()
			cursorData.execute(sqlQuery)

			numberofColumns = len(cursorData.description)
			#Create the header
	#		header = ""
	#		for des in cursorData.description:
	#			header += des[0]+','
	#		header = header[:-1]+"\n"
	#		outputFile.write(header)

			for data in cursorData.fetchall():
				rowString = ''
				for num in range(1, numberofColumns):
					rowString += str(data[num])+','
				rowString = rowString[:-1]+"\n"
				outputFile.write(rowString)

	if outputFile:
		outputFile.close
	if cursorData:
		cursorData.close()
	cursor.close()
	if fileSet:
		finalTimeStamp = "{0}".format(fileSet.DataTimeStamp)

	#print "Final row timestamp: ", finalTimeStamp

finally:
	cnxn.close()

	if finalTimeStamp:
		cntlFile.seek(0)
		cntlFile.truncate()
		cntlFile.write(finalTimeStamp)
		cntlFile.write("\n")
		cntlFile.close

