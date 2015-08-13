from QueryCSVTransform import QueryCSVTransform2Stage

if __name__ == "__main__":
        params = {}
        params["controlfile"]= "/Sensorbouy/SensorControl/CurrentbyDepthDateFile.txt"
        params["outputpath"] = "/Sensorbouy/SensorDump/"
        params["dbhost"]="192.168.2.219"
        params["dbuser"]='sa'
        params["dbpassword"]='syxaV8L5X2'
        params["dbname"] ='AXYSDMS'
        params["queryString1"] = """with ctestuff 
                as (
                SELECT distinct [HeadDepth]
                   + [BlankingDistance] 
                   + [BinSpacing]/2 
                   + [BinSpacing]*(DetailOrder - 1) as Depth 
                FROM [AXYSDMS].[dbo].[axDMSPluginADCPBinDetails] bd 
                JOIN [AXYSDMS].[dbo].[axDMSPluginADCPBinHeader] bh on bh.BinHeaderDBID = bd.BinHeaderDBID 
                WHERE bh.[ModifyDate] > dateadd(hour, -1, '{0}')
                ) 
                select stuff((select ', Csp'+convert(varchar, depth)+', Cdr'+convert(varchar, depth)
                    from ctestuff 
                    order by depth 
                    for XML PATH('') 
                ) ,1,1,'') as sqlString;"""
        params["queryString2"] = """select convert(varchar(19), obsdate, 121) as DataTimeStamp, {1}
                from (SELECT bh.[ModifyDate] obsdate, col, value 
                  FROM [AXYSDMS].[dbo].[axDMSPluginADCPBinDetails] bd 
                  JOIN [AXYSDMS].[dbo].[axDMSPluginADCPBinHeader] bh on bh.BinHeaderDBID = bd.BinHeaderDBID 
                    cross apply 
                    ( select velocity as value, REPLACE('Csp'+convert(varchar,[HeadDepth]
                        + [BlankingDistance] 
                        + [BinSpacing]/2 
                        + [BinSpacing]*(DetailOrder - 1)), '.', '_') as col
                    union all 
                    select direction as value, REPLACE('Cdr'+convert(varchar,[HeadDepth] 
                        + [BlankingDistance] 
                        + [BinSpacing]/2  
                        + [BinSpacing]*(DetailOrder - 1)), '.', '_') as col
                    ) c (value, col) 
                where bh.[ModifyDate] >= '{0}') d 
                pivot 
                (max(value) 
                    for col in ({1})
                )  piv 
                where obsdate > '{0}'"""
        params["fileprefix"] = "current"
        
        #print params
        qcsvwriter = QueryCSVTransform2Stage(**params)
        qcsvwriter.run()
        print "finished"
