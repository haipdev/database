import logging
from asgiref.sync import sync_to_async
import pyodbc
import haip.config as config
from haip.database.driver import DbDriver, DatabaseException

logger = logging.getLogger(__name__)

class Database(DbDriver):
    async def connect(self):
        cfg = config.get('databases', self.db_name, 
                         database=config.MANDATORY,
                         host='127.0.0.1', port=1433,
                         username=config.MANDATORY, password=config.MANDATORY,
                         driver=config.MANDATORY,
                         autocommit=True)
        try:
            self.conn = await sync_to_async(pyodbc.connect)(DRIVER=cfg.driver,
                                                            SERVER=f'{cfg.host},{cfg.port}',
                                                            DATABASE=cfg.database,
                                                            UID=cfg.username,
                                                            PWD=cfg.password)
        except pyodbc.DatabaseError as e:
            raise DatabaseException(str(e))
        self.conn.autocommit = cfg.autocommit
        logger.debug("connected to database '%s'", self.db_name)

