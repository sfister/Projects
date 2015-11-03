import logging
import hashlib
import smtplib
from smtplib import SMTPException

from geoalchemy import WKTSpatialElement

from base import SQLConnectionBase

class ObsUpdateBase(SQLConnectionBase):
    """
    Inserts or updates data in the obs database
    data: A list of dicts representing each record to be stored,
          Eacg Dict must contain the keys: 
          site: if a null value it will be replaced by a 8 chars hash based on lat lon
          product: A product id
          time: a datetime object
          lon: longitude as float
          lat: latitude as float
          and the rest of the fields to popolate in each key.
    """
    def __init__(self, host, username, password, table, data, database='obs',
                 port=None, logger=logging, fake=False, **kwargs):
        super(ObsUpdateBase, self).__init__(host, database, 
                                            username=username,
                                            password=password,
                                            port=port,
                                            logger=logger,**kwargs)
        self.fake = fake
        self.table = table
        self.data = data

    def _get_table(self, table):
        return getattr(self.tables, table)

    def _format_values(self, product, time, lon, lat, site=None, **data):
        if not site:
            site = hashlib.md5('%.3f_%.3f'%(lon,lat)).digest().encode('base64')[:8]
        obsid = site + time.strftime("%Y%m%d%H%M%S")+'_%.3f_%.3f' % (lon, lat)
        point = WKTSpatialElement('POINT (%f %f)' % (lon, lat))
        time = time.strftime('%Y-%m-%d %H:%M:%S')

        values = dict(id=obsid, point=point, time=time, 
                      lon=lon, lat=lat, site=site, 
                      product=product)
        # Remove unknown data
        for key in data.keys():
            if not hasattr(self.table, key):
                data.pop(key)

        values.update(**data)
        return values

    def _update(self, values):
        record = self.session.query(self.table).get(values['id'])
        if record:
            for field, val in values.items():
                setattr(record, field, val)
        else:
            self.session.add(self.table(**values))

    def _perform_sql(self):
        try: 
            self.table = self._get_table(self.table)
            for data in self.data:
                self.logger.debug("Data to store in db: %s" % data)
                values = self._format_values(**data)
                self._update(values)
        except:
            self.session.rollback()
            self.logger.error('Error Storing data in database, rolling back.')
            raise
        else:
            if not self.fake:
                self.session.commit()
                self.logger.info('Recorded %s rows in the database' % len(self.data))
            else:
                self.logger.info('Fake recorded %s rows in the database' % len(self.data))


class CheckObsFeed(SQLConnectionBase):
    """This class will query the last obs updates and give a report on which
    observation feeds show a gap bigger the tolerance
    """
    
    message = """
From: From Alerts <alerts@metocean.co.nz>
To: To Alerts <alerts@metocean.co.nz>
MIME-Version: 1.0
Content-type: text/html
Subject: [WARN] Observations feed gaps
This is an e-mail message to be sent in HTML format
<b>This is HTML message.</b>
<h1>This is headline.</h1>
"""        
    def __init__(self, host, username, password, 
                 feeds, 
                 email_to=['alerts@metocean.co.nz'],
                 email_host='localhost',
                 email_from='alerts@metocean.co.nz',
                 database='obs',
                 port=None, logger=logging, **kwargs):
        super(CheckObsFeed, self).__init__(host, database, 
                                            username=username,
                                            password=password,
                                            port=port,
                                            logger=logger,**kwargs)
        self.feeds = feeds
        self.email_from = email_from
        self.email_to = email_to
        self.email_host = email_host       

    def _perform_sql(self):
        self.all_gaps = {}
        for feed in self.feeds:
            table = self.tables.get(feed.pop('table'))
            tolerance = feed.pop('tolerance')
            query = self.session.query(table).filter_by(**feed).order_by('time')
            print query
            gaps = []
            querysize = query.count()
            if querysize > 1:
                maxquery = min(10,querysize)
                for r,record in enumerate(query[1:maxquery]):
                    previous = query[r]
                    gap = ((record.time - previous.time).seconds)/60
                    print record.time, previous.time, record.site, record.product
                    if gap > tolerance:
                        gaps.append((previous.time, record.time))
                obs_name = '%s_%s_%s' % (table.__name__, record.product, record.site)
                self.all_gaps[obs_name] = gaps

    def _format_email(self):
        rows = []
        
        for feed, gaps in self.all_gaps.items():
            row = [feed]
            row.extend(gaps)
            rows.append(row)
        
        table = "<table>%s</table>" % ()
        

    def run(self):
        super(CheckObsFeed, self).run()
        try:
           smtpObj = smtplib.SMTP(self.email_host)
           print self.all_gaps
           smtpObj.sendmail(self.email_from, self.email_to, self.message)         
           print "Successfully sent email"
        except SMTPException as sm:
           print "Error: unable to send email"
           print sm
           