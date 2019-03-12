import logging
import mysql.connector
import haip.config as config
from haip.database.driver import DbDriver, DatabaseException

logger = logging.getLogger(__name__)

class Database(DbDriver):
    async def connect(self):
        cfg = config.get('databases', self.db_name, 
                         database=config.MANDATORY,
                         host='127.0.0.1', port=3306,
                         username=config.MANDATORY, password=config.MANDATORY,
                         autocommit=True, keep_alive=True)
        try:
            self.conn = mysql.connector.connect(database=cfg.database, host=cfg.host, port=cfg.port,
                                                user=cfg.username, password=cfg.password)
        except mysql.connector.errors.InterfaceError as e:
            raise DatabaseException(str(e))
        self.conn.raise_on_warnings = True
        self.conn.autocommit = cfg.autocommit
        logger.debug("connected to database '%s'", self.db_name)

