import os
import logging
import asyncio
import pytest
import haip.config as config
import haip.database as database
import haip.database.pool as pool

logging.basicConfig()
logging.getLogger('haip').setLevel(logging.DEBUG)

basedir = os.path.dirname(__file__)

@pytest.fixture
def setup():
    config.load(basedir + os.sep + 'etc', 'dev')
    config.set(template_dir=basedir+os.sep+'templates')

@pytest.fixture(scope="module", autouse=True)
@pytest.mark.asyncio
def teardown(request):
    def shutdown():
        async def async_shutdown():
            await pool.shutdown()
        loop = asyncio.get_event_loop() 
        loop.run_until_complete(async_shutdown())    
    request.addfinalizer(shutdown)

@pytest.mark.asyncio
async def test_simple(setup):
    rows = await database.query('test_mysql', 'queries/test_mysql_select.sql')
    assert rows

@pytest.mark.asyncio
async def test_sequence(setup):
    db_name = 'test_mysql'

    # 1 delete users in scope (propably empty set)
    affected = await database.do(db_name, 'queries/test_mysql_delete.sql')    
    rows = await database.query(db_name, 'queries/test_mysql_select.sql')
    assert not rows

    # 2 insert an user
    affected = await database.do(db_name, 'queries/test_mysql_insert.sql', firstname='Test', lastname='Tester')
    assert affected == 1
    row = await database.query_first(db_name, 'queries/test_mysql_select.sql')
    assert 'firstname' in row

    # 3 update this user
    affected = await database.do(db_name, 'queries/test_mysql_update.sql', firstname='Test2', lastname='Tester')
    assert affected == 1
    rows = await database.query_assoc(db_name, 'queries/test_mysql_select.sql')
    assert rows[0].firstname == 'Test2'

    # 4 call a function
    rows = await database.query(db_name, 'queries/test_mysql_function.sql')
    assert rows[0][0] == 'Tester'

@pytest.mark.asyncio
async def test_mysql_proc(setup):
    db_name = 'test_mysql'
    # 4 call procedure
    await database.call(db_name, 'testproc')
    assert True



