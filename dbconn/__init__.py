import sys
import urllib
import yaml

import pyodbc
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# DECLARATIONS FOR SETUP.PY
APP_NAME = 'dbconn'
__versionnum__ = ('0', '0', '1')
APP_VERSION = '.'.join([i for i in __versionnum__])

# CONNECTION CLASS
class DBconn():

    '''Class to handle the connections and session with the DB'''

    def __init__(self, db_conf):
        self.db_conf = db_conf.upper()
        self.engine = sa.create_engine(self.get_connection_string())

    def get_connection_string(self):

        with open('dbconf.yaml') as f:
            conf = yaml.safe_load(f)

        if sys.platform == 'linux':
            return 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus((
                       'DRIVER=FreeTDS;'
                       'SERVER={server};'
                       'PORT={port};'
                       'DATABASE={db};'
                       'UID={uid};'
                       'PWD={pwd};'
                       'TDS_Version={tds_v};'
                    ).format(
                        server = conf[self.db_conf]['SERVER'],
                        port   = conf[self.db_conf]['PORT'],
                        db     = conf[self.db_conf]['DBNAME'],
                        uid    = conf[self.db_conf]['USERNAME'],
                        pwd    = conf[self.db_conf]['PASSWORD'],
                        tds_v  = conf[self.db_conf]['TDS_VERSION']
                    ))
        else:
            return 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus((
                       'DRIVER=FreeTDS;'
                       'SERVER={server};'
                       'PORT={port};'
                       'DATABASE={db};'
                       'UID={uid};'
                       'PWD={pwd};'
                    ).format(
                        server = conf[self.db_conf]['SERVER'],
                        port   = conf[self.db_conf]['PORT'],
                        db     = conf[self.db_conf]['DBNAME'],
                        uid    = conf[self.db_conf]['USERNAME'],
                        pwd    = conf[self.db_conf]['PASSWORD'],
                    ))

    def Base(self):
        return declarative_base(self.engine)

    def get_session(self):
        Session = sessionmaker(bind=self.engine)
        return Session()

class CtrlSession():
    def __init__(self, engine):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def __enter__(self):
        return self.session

    def __exit__(self, e_type, e_value, e_tback):
        # TODO: evaluate response to know if we need to commit, rollback or
        # close the session 
        self.session.close()
