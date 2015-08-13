from QueryCSVTransform import QueryCSVTransform

if __name__ == "__main__":
        params = {}
        params["controlfile"]= "/Sensorbouy/SensorControl/WindDateFile.txt"
        params["outputpath"] = "/Sensorbouy/SensorDump/"
        params["dbhost"]="192.168.2.219"
        params["dbuser"]='sa'
        params["dbpassword"]='syxaV8L5X2'
        params["dbname"] ='AXYSDMS'
        params["queryString"] = """SELECT convert(datetime, convert(varchar(14), oe.[DataTimeStamp], 121)+case when datepart(MINUTE, oe.[DataTimeStamp]) < 30 then '00' 
           else '30' end , 121) as DataTimeStamp, [Last sampling interval gust speed] as windGust 
      ,[Average wind speed] as windSpeedAvg 
      ,[Average wind direction] as windDirection
          ,(select -1.0*(convert(float, substring(latitude, 0, charindex(subdegrees, latitude))) + convert(float, subdegrees)/60.0) 
       from (
         select reverse(substring(reverse(latitude), 2, 7)) as subdegrees, latitude
           from ( select top 1 latitude 
          from [AXYSDMS].[dbo].[axDHDP_AXYSGPSGeneric10902] a  where DataTimeStamp < oe.dataTimeStamp 
           and Latitude is not null and Latitude <> '' order by dataTimeStamp desc) a) b) as  Latitude  
        ,(select convert(float, substring(Longitude, 0, charindex(subdegrees, Longitude))) + convert(float, subdegrees)/60.0 
       from (
         select reverse(substring(reverse(Longitude), 2, 7)) as subdegrees, Longitude
           from ( select top 1 Longitude 
          from [AXYSDMS].[dbo].[axDHDP_AXYSGPSGeneric10902] where DataTimeStamp < oe.dataTimeStamp 
           and Latitude is not null and Longitude <> '' order by dataTimeStamp desc) a) b) as  Longitude
  from [AXYSDMS].[dbo].[axDHDP_AXYSTechnologiesIncTRIAXYSOEM11800] oe 
  LEFT OUTER join [AXYSDMS].[dbo].[axDHDP_GillVaisalaRMYoungSerialAnemometer43100] ws on ws.DataTimeStamp = oe.DataTimeStamp 
  where ws.DataTimeStamp > '{0}'
    order by oe.[DataTimeStamp]"""
        params["fileprefix"] = "wind"
        
        qcsvwriter = QueryCSVTransform(**params)
        qcsvwriter.run()
        print "finished"

