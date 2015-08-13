from QueryCSVTransform import QueryCSVTransform

if __name__ == "__main__":
        params = {}
        params["controlfile"]= "/Sensorbouy/SensorControl/WaveDateFile.txt"
        params["outputpath"] = "/Sensorbouy/SensorDump/"
        params["dbhost"]="192.168.2.219"
        params["dbuser"]='sa'
        params["dbpassword"]='syxaV8L5X2'
        params["dbname"] ='AXYSDMS'
        params["queryString"] = """SELECT convert(datetime, convert(varchar(14), DataTimeStamp, 121)+case when datepart(MINUTE, datatimestamp) < 30 then '00' 
               else '30' end , 121) as DataTimeStamp, Havg, Tz,Hmax,Hsig,Tsig,MeanPeriod,PeakPeriod,MeanMagneticDirection,MeanSpread,WaveSteepness,
            (select -1.0*(convert(float, substring(latitude, 0, charindex(subdegrees, latitude))) + convert(float, subdegrees)/60.0) 
               from (
                 select reverse(substring(reverse(latitude), 2, 7)) as subdegrees, latitude
                   from ( select top 1 latitude 
              from [axDHDP_AXYSGPSGeneric10902] where DataTimeStamp < ws.dataTimeStamp 
               and Latitude is not null and Latitude <> '' order by dataTimeStamp desc) a) b) as  Latitude, 
            (select convert(float, substring(Longitude, 0, charindex(subdegrees, Longitude))) + convert(float, subdegrees)/60.0
               from (
                 select reverse(substring(reverse(Longitude), 2, 7)) as subdegrees, Longitude
                   from ( select top 1 Longitude 
              from [axDHDP_AXYSGPSGeneric10902] where DataTimeStamp < ws.dataTimeStamp 
               and Latitude is not null and Longitude <> '' order by dataTimeStamp desc) a) b) as  Longitude
                 FROM [AXYSDMS].[dbo].[axDMSPluginTRIAXYSWaveStatistics] ws
          where datatimestamp > '{0}' 
          order by DataTimeStamp"""
        params["fileprefix"] = "wave"
        
        qcsvwriter = QueryCSVTransform(**params)
        qcsvwriter.run()
        print "finished"

