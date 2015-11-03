import obs
import logging
from base import SQLConnectionBase
from datetime import datetime, timedelta
from sqlalchemy import and_, or_, func


class MonitorObs(SQLConnectionBase):
    def _perform_sql(self):
        
        filter = {}
        filter["last_check"] = "now()"
        query = self.session.query(self.tables.monitor_obs)\
        .add_column((func.datediff(self.tables.monitor_obs.last_check, func.now())).label("test"))\
        .filter(self.tables.monitor_obs.locked == False)\
        .filter(func.datediff(self.tables.monitor_obs.last_check, func.now()) <= self.tables.monitor_obs.frequency) \
        .order_by('last_check')
        logger.debug(query)

        
if __name__ == "__main__":

    logging.basicConfig( \
    format='%(asctime)s %(levelname)s %(threadName)s %(filename)s(%(lineno)s)-%(funcName)s %(message)s '\
    , level=logging.DEBUG)
    
    logger = logging.getLogger()
    
    mobs = MonitorObs(host="10.1.1.156", database="metocean", \
                               username="metocean", \
                               password="oceans11",  \
                               port="3306", \
                               logger=logger)
    
    mobs.run()
    
    #obCheck = obs.CheckObsFeed(host="10.1.1.156", database="obs", \
    #                           username="metocean", \
    #                           password="oceans11",  \
    #                           port="3306", \
    #                           feeds=[{"table": "wave", "tolerance": "3", "product":"maari", "site": "maari"}], \
    #                           email_to="s.fister@metocean.co.nz", \
    #                           email_host="10.1.1.156", \
    #                           logger=logger)
    
    #obCheck.run()
    
    print "finish"