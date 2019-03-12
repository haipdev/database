import logging
import importlib 
import asyncio
import haip.config as config
from haip.database.driver import DatabaseException

logger = logging.getLogger(__name__)

class DatabasePoolExhaustedException(DatabaseException):
    pass

_pool = {}

async def _new_dbi(db_name):
    dbconfig = config.get('databases', db_name, type=config.MANDATORY)
    module = f'haip.database.drivers.{dbconfig.type}'    
    try:  # import database driver
        dbdriver = importlib.import_module(module)
    except ModuleNotFoundError:
        raise DatabaseException(f"database implementation for db '{db_name}' (with type {dbconfig.type}) not found")
    try:  # instantiate the database driver
        dbi = dbdriver.Database(db_name)
    except AttributeError:
        raise DatabaseException(f'no Database class found in "{module}"')
    await dbi.connect()
    logger.debug(f'new database connection to "{db_name}" established')
    return dbi

async def acquire(db_name):
    if db_name not in _pool:
        _pool[db_name] = {
            'open': 0,
            'idle': []
        }
    try:
        dbi = _pool[db_name]['idle'].pop()
        logger.debug(f'use existing idle connection for "{db_name}"')
        return dbi
    except IndexError:
        pass
    cfg = config.get('databases', db_name, max_connections=3)
    if _pool[db_name]['open'] >= cfg.max_connections:
        raise DatabasePoolExhaustedException(f"max_connections reached for {db_name}")
    dbi = await _new_dbi(db_name)
    _pool[db_name]['open'] += 1
    return dbi

async def release(dbi):
    cfg = config.get('databases', dbi.db_name, max_idle_connections=3)
    if len(_pool[dbi.db_name]['idle']) < cfg.max_idle_connections:
        _pool[dbi.db_name]['idle'].append(dbi)
    else:
        await dbi.disconnect()

async def shutdown():
    logger.info('close all open idle db-connections')
    for _, pool in _pool.items():
        for dbi in pool['idle']:
            await dbi.disconnect()

    
