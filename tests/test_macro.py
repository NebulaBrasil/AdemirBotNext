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

