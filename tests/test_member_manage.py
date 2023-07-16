import pytest
from interactions import Client, Guild, Member
from interactions import SlashContext, ModalContext
from extensions.member_manage import MemberManage

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def guild(client):
    return Guild(client=client, id=123123, owner_id=123123, name='fake', preferred_locale='pt-BR')

@pytest.fixture
def member_manage(client):
    return MemberManage(client)

@pytest.fixture
def member_ids():
    return [123, 456, 789]

@pytest.fixture
def member_objects(client, member_ids):
    return [Member(client=client, guild_id=123123, id=member_id) for member_id in member_ids]


@pytest.fixture
def slash_context(client):
    return SlashContext(client=client)

@pytest.fixture
def modal_context(client):
    return ModalContext(client=client)

@pytest.fixture
def fectch_member(member_objects, member_ids):
    async def fetch_memb(id):
        return member_objects[member_ids.index(id)]
    return fetch_memb

@pytest.mark.asyncio
async def test_ban_members(mocker, member_manage, guild, fectch_member, member_ids):    
    ban_mock = mocker.patch("interactions.Guild.ban")
    guild.fetch_member = fectch_member
    await member_manage.ban_members(guild, member_ids)
    assert ban_mock.call_count == len(member_ids)

@pytest.mark.asyncio
async def test_kick_members(mocker, member_manage, guild, fectch_member, member_ids):
    guild.fetch_member = fectch_member    
    kick_mock = mocker.patch("interactions.Guild.kick")
    await member_manage.kick_members(guild, member_ids)
    assert kick_mock.call_count == len(member_ids)

def test_split_and_parse_member_ids(member_manage):
    member_ids = "123\n456\n789"
    result = member_manage.split_and_parse_member_ids(member_ids)
    assert result == [123, 456, 789]