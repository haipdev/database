import os
import pytest
import haip.config as config
import haip.database as database

basedir = os.path.dirname(__file__)

@pytest.fixture
def setup():
    config.load(basedir + os.sep + 'etc', 'dev')
    config.set(template_dir=basedir+os.sep+'templates')

@pytest.mark.skip(reason="you need a running db server for this test")
@pytest.mark.asyncio
async def test_mssql(setup):
    db_name = 'test_mssql'
    row = await database.query_first(db_name, 'queries/test_mssql_select.sql')
    assert 'SQL Server' in row.version 


