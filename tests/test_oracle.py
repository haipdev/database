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
async def test_oracle(setup):
    db_name = 'test_oracle'
    rows = await database.query(db_name, 'queries/test_oracle_select.sql')
    assert rows


