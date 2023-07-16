import pytest
from interactions import Client, Guild, InteractionType, Member
from interactions import SlashContext, ModalContext
from extensions.member_manage import MemberManage

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def guild(client, fetch_member):
    guild = Guild(client=client, id=123123, owner_id=123123, name='fake', preferred_locale='pt-BR')
    client.cache.place_guild_data({
        "id": 123123,
        "name": "test_guild",
        "icon": "",
        "splash": "",
        "discovery_splash": "",
        "owner_id": "123456789012345678",
        "afk_channel_id": None,
        "afk_timeout": 0,
        "verification_level": 0,
        "default_message_notifications": 0,
        "explicit_content_filter": 0,
        "roles": [],
        "emojis": [],
        "features": [],
        "mfa_level": 0,
        "application_id": None,
        "system_channel_id": None,
        "system_channel_flags": 0,
        "rules_channel_id": None,
        "vanity_url_code": None,
        "description": None,
        "banner": None,
        "premium_tier": 0,
        "preferred_locale": "en-US",
        "public_updates_channel_id": None,
        "nsfw_level": 0,
        "stickers": [],
        "premium_progress_bar_enabled": False,
    })
    guild.fetch_member = fetch_member
    return guild

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
    slash_context = SlashContext.from_dict(client, {
        "id":1234,
        "type":InteractionType.APPLICATION_COMMAND,
        "channel_id": 123412, 
        "guild_id": 123123, 
        "locale":"pt-BR", 
        "token":"dummy",
        "data": {"id":99898, "name":"name"},
        "user":{"id":123123, "username":"fulano", "avatar": "", "discriminator":123123}
        })
    return slash_context

@pytest.fixture
def modal_context(client):
    return ModalContext(client=client)

@pytest.fixture
def fetch_member(member_objects, member_ids):
    async def fetch_memb(id):
        if id not in member_ids:
            return None
        else:
            return member_objects[member_ids.index(id)]
    return fetch_memb

@pytest.mark.asyncio
async def test_ban_members(mocker, member_manage, guild, fetch_member, member_ids):    
    ban_mock = mocker.patch("interactions.Guild.ban")
    guild.fetch_member = fetch_member
    await member_manage.ban_members(guild, member_ids)
    assert ban_mock.call_count == len(member_ids)
    await member_manage.ban_members(guild, [1])
    assert ban_mock.call_count == len(member_ids)

@pytest.mark.asyncio
async def test_kick_members(mocker, member_manage, guild, fetch_member, member_ids):
    guild.fetch_member = fetch_member
    kick_mock = mocker.patch("interactions.Guild.kick")
    await member_manage.kick_members(guild, member_ids)
    assert kick_mock.call_count == len(member_ids)
    await member_manage.kick_members(guild, [1])
    assert kick_mock.call_count == len(member_ids)

def test_split_and_parse_member_ids(member_manage):
    member_ids = "123\n456\n789"
    result = member_manage.split_and_parse_member_ids(member_ids)
    assert result == [123, 456, 789]

@pytest.fixture
def send_modal():
    async def send_modal(modal):
        return None
    return send_modal

@pytest.fixture
def wait_for_modal(client):
    async def wait_for_modal(modal):
        ctx = ModalContext(client)
        ctx.responses = dict.fromkeys(["members"], "123\n456\n789")
        return ctx
    return wait_for_modal

@pytest.mark.asyncio
async def test_mass_ban(mocker, client, member_manage, slash_context, send_modal, wait_for_modal, fetch_member, guild):
    member_ids = [123, 456, 789]    
    guild.fetch_member = fetch_member
    mock_ban_members = mocker.patch("extensions.member_manage.MemberManage.ban_members")
    mock_modal_ctx_send = mocker.patch("interactions.ModalContext.send")
    client.wait_for_modal = wait_for_modal
    slash_context.send_modal = send_modal
    await member_manage.mass_ban(slash_context)
    mock_ban_members.assert_called_once_with(guild, member_ids)
    mock_modal_ctx_send.assert_called_once_with(f"{len(member_ids)} usuários banidos.")

@pytest.mark.asyncio
async def test_mass_kick(mocker, client, member_manage, slash_context, send_modal, wait_for_modal, fetch_member, guild):
    member_ids = [123, 456, 789]    
    guild.fetch_member = fetch_member
    mock_kick_members = mocker.patch("extensions.member_manage.MemberManage.kick_members")
    mock_modal_ctx_send = mocker.patch("interactions.ModalContext.send")
    client.wait_for_modal = wait_for_modal
    slash_context.send_modal = send_modal
    await member_manage.mass_kick(slash_context)
    mock_kick_members.assert_called_once_with(guild, member_ids)
    mock_modal_ctx_send.assert_called_once_with(f"{len(member_ids)} usuários expulsos.")