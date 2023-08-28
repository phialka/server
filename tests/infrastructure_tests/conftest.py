import pytest
from app import repo

@pytest.fixture()
async def test_db():
    await repo.activate_database("postgresql://postgres:toor@127.0.0.1:5432/testdb")

    yield

    await repo.inactivate_database()