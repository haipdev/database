import os
import logging
from asgiref.sync import sync_to_async
import cx_Oracle
import haip.config as config
from haip.database.driver import DbDriver, DatabaseException

logger = logging.getLogger(__name__)

class Database(DbDriver):
    async def connect(self):
        cfg = config.get('databases', self.db_name, 
                         host='127.0.0.1', port=1521,
                         username=config.MANDATORY, password=config.MANDATORY,
                         autocommit=True,
                         service_name=None, sid=None)
        if cfg.service_name is None:
            if cfg.sid is None:
                raise AttributeError(f'neither service_name or sid in configuration (dbname="{self.db_name})"')
            dsn_tns = cx_Oracle.makedsn(cfg.host, cfg.port, cfg.sid)
        else:
            dsn_tns = cx_Oracle.makedsn(cfg.host, cfg.port, service_name=cfg.service_name)

        os.environ['NLS_LANG'] = 'GERMAN_GERMANY.WE8MSWIN1252'
        self.conn = await sync_to_async(cx_Oracle.connect)(cfg.username, cfg.password, dsn_tns)
        self.conn.autocommit = cfg.autocommit
        logger.debug('connected to database "%s"', self.db_name)

