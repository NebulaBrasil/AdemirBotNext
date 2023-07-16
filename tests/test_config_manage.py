import asyncio
import interactions
import pytest
from interactions import Client, Guild, InteractionType, Member, Role, SlashCommand
from interactions import SlashContext
from extensions.config_manage import ConfigManage

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
def config_manage(client):
    return ConfigManage(client)

@pytest.fixture
def cargo(client):
    cargo = Role.from_dict({
        "id": 123,
        "guild_id": 123123,
        "name": "Cargo",
        "color":"#101010",
        "position":1,
        "purchasable_or_has_subscribers":True,
        "permissions": interactions.Permissions.SEND_MESSAGES
    }, client)
    return cargo

@pytest.fixture
def slash_context(client, cargo):
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
    slash_context.args = [cargo]
    slash_context.kwargs = {"cargo":cargo}
    return slash_context

@pytest.mark.asyncio
async def test_configure_conversation_role(mocker, config_manage, cargo, slash_context):
    mock_slash_ctx_send = mocker.patch("interactions.SlashContext.send")
    mock_slash_ctx_defer = mocker.patch("interactions.SlashContext.defer")    
    mock_repo_set = mocker.patch("repository.ademir_cfg_repository.AdemirCfgRepository.set_guild_conversation_role")
    await config_manage.configure_conversation_role(slash_context, cargo)
    assert mock_slash_ctx_defer.call_count == 1    
    mock_slash_ctx_send.assert_called_once_with(f"Cargo <@&{cargo.id}> permitido para o Ademir configurado.", ephemeral=True)