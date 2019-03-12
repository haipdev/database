import logging

logger = logging.getLogger(__name__)

import abc
import haip.config as config

class DatabaseException(Exception):
    def __init__(self, msg):
        logger.error("%s : %s", self.__class__.__name__, msg)
        super().__init__(msg)

class _RowContainer(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("RowContainer - No such attribute: " + name)

class DbDriver(abc.ABC):
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    @abc.abstractmethod
    async def connect(self):
        pass

    async def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    async def query(self, query, *values, assoc=False):
        rows = await self._run_cursor(query, *values, is_query=True, assoc=assoc)
        return rows

    async def do(self, query, *values):
        return await self._run_cursor(query, *values, is_query=False)    

    async def _run_cursor(self, query, *values, is_query=True, assoc=False):
        cursor = None
        try:
            cursor = self.conn.cursor()
            logger.debug('CURSOR query: %s', query)
            cursor.execute(query, values)
            if is_query:
                result = cursor.fetchall()
                if assoc:
                    result = self._dictify(cursor, result)
            else:
                result = cursor.rowcount
            cursor.close()
            return result
        except AttributeError as error:
            if cursor is not None:
                cursor.close()
            raise DatabaseException(str(error))

    async def call(self, procedure):
        cursor = None
        try:
            cursor = self.conn.cursor()
            logger.debug('Call procedure: %s', procedure)
            cursor.callproc(procedure)
            cursor.close()
        except Exception as error:
            if cursor is not None:
                cursor.close()
            raise DatabaseException(str(error))

    def _dictify(self, cursor, rows):
        if not rows:
            return rows
        headers = [d[0].lower() for d in cursor.description]
        rows_assoc = []
        for row in rows:
            row_dict = _RowContainer()
            for i, value in enumerate(row):
                row_dict[headers[i]] = value
            rows_assoc.append(row_dict)
        return rows_assoc




