import logging

import haip.config as config
import haip.template as template
from haip.database import pool

logger = logging.getLogger(__name__)

#TODO: use decorator

async def query(db_name, query_template, *values, **args):
    dbi = await pool.acquire(db_name)
    query = await template.render(query_template, **args)
    rows = await dbi.query(query, *values)
    await pool.release(dbi)
    return rows

async def query_assoc(db_name, query_template, *values, **args):
    dbi = await pool.acquire(db_name)
    query = await template.render(query_template, **args)
    rows = await dbi.query(query, *values, assoc=True)
    await pool.release(dbi)
    return rows

async def query_first(db_name, query_template, *values, **args):
    rows = await query_assoc(db_name, query_template, *values, **args)
    if rows:
        return rows[0]
    return None

async def do(db_name, query_template, *values, **args):
    dbi = await pool.acquire(db_name)
    query = await template.render(query_template, **args)
    result = await dbi.do(query, *values)
    await pool.release(dbi)
    return result

async def call(db_name, procedure):
    dbi = await pool.acquire(db_name)
    result = await dbi.call(procedure)
    await pool.release(dbi)
    return result

async def shutdown():
    await pool.shutdown()

