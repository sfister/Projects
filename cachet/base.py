import os
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import update

class SQLConnectionBase(object):
    """Base class for any sql connection."""
    def __init__(self, host, database, username, password=None,
                 dialect='mysql',  
                 port=None,
                 logger=logging, 
                 automap=True,
                 fake=False,
                 **kwargs):
        super(SQLConnectionBase, self).__init__()
        self.dialect = dialect
        self.host = host
        self.database = database
        self.username = username
        self.password = password
        self.port = port
        self.logger = logger
        self.automap = automap
        self._build_dburi()
        self._build_sql_command()
        
    def get_fields(self, table, fields):
        fields_objs = {}
        if table in self.tables.keys():
            table_obj = getattr(self.tables, table)
            for field in fields:
                if hasattr(table_obj, field):
                    fields_objs[field] = getattr(table_obj, field)
                else:
                    self.logger.warning('Field (%s) could not be foun in %s table from %s database.' % (field, table, self.database))
        return fields_objs

    def _automap(self):
        self.logger.debug('Automapping database...')
        self._base = automap_base()
        self._base.prepare(self.engine, reflect=True)
        self.tables = self._base.classes

    def _build_dburi(self):
        dburi = self.dialect + '://' + self.username 
        if self.password:
            dburi += ':' + self.password 
        dburi += '@' + self.host
        if self.port:
            dburi += ':' + str(self.port)
        dburi += "/"+self.database
        self.dburi = dburi
        return dburi

    def _establish_connection(self):
        self.engine = create_engine(self.dburi)
        if self.automap:
            self._automap()
        self.session = Session(self.engine)
        self.logger.debug('Established connection with %s://%s@%s/%s' % \
                (self.dialect, self.username, self.host, self.database))

    def _build_sql_command(self):
        pass

    def _perform_sql(self):
        self.result = None

    def run(self):
        try:
            self._establish_connection()
        except:
            if hasattr(self, 'session'):
                self.session.rollback()
            raise
        else:
            self._perform_sql()
        finally:
            if hasattr(self, 'session'):
                self.session.close()
                self.logger.debug('Closed connection with with %s://%s@%s/%s' % \
                                  (self.dialect, self.username, self.host, self.database))

class SQLStatement(SQLConnectionBase):
    """Base class to perform Raw sql statements"""
    def __init__(self, dialect, host, database, username, password,
                 raw_sql,
                 logger=logging,
                 port=None,
                 automap=False,
                 **kwargs):
        super(SQLStatement, self).__init__(dialect, host, database, username,
                                           password,
                                           port=port,
                                           logger=logger,
                                           automap=automap,
                                           **kwargs)
        self.raw_sql = raw_sql

    def _perform_sql(self):
        if isinstance(self.raw_sql, (str,unicode)):
            self.logger.info('Executing "%s"' % self.raw_sql)
            result = self.engine.execute(raw_sql)
        elif isinstance(self.raw_sql, (list)):
            result = []
            for sql in self.raw_sql:
                self.logger.info('Executing "%s"' % sql)
                result.append(self.engine.execute(sql))
        self.result = result

class SQLSelectDump(SQLConnectionBase):
    """Simple data select and dump to a text file"""
    def __init__(self, dialect, host, database, username, password,
                 table,
                 fields,
                 dump_to='sql_dump.csv',
                 logger=logging, 
                 port=None,
                 dump_format='csv',
                 id=None, 
                 conditions=None, 
                 order_by=None, 
                 filter_by=None,
                 **kwargs):
        super(SQLSelectBase, self).__init__(dialect, host, database, username, 
                                            password,
                                            port=port,
                                            logger=logger)

    def _build_sql_command(self):
        pass

    def _perform_sql(self):
        pass

class SQLInsertBase(SQLConnectionBase):
    """docstring for SQLPull"""
    def __init__(self, table, data, **kwargs):
        super(SQLInsertBase, self).__init__()
        self.table = table
        self.data = data

class SQLCleanUpBase(SQLConnectionBase):
    """docstring for SQLPull"""
    def __init__(self,table, fields, **kwargs):
        super(SQLCleanUpBase, self).__init__()
        self.arg = arg


class SQLArchive(SQLConnectionBase):
    """docstring for SQLArchive"""
    def __init__(self, arg):
        super(SQLArchive, self).__init__()
        self.arg = arg