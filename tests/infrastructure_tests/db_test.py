import pytest
from app import repo



async def test_user_addget(test_db):
    usr_added = await repo.User.add(name="sasha", shortname="sh1")

    usr_getted = await repo.User.get(user_id=usr_added.id)

    assert len(usr_getted) == 1
    assert usr_added == usr_getted[0]