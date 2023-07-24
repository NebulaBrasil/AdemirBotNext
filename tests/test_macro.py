import json
from unittest.mock import MagicMock
import interactions
import pytest
from extensions.macro import Macros
from interactions import Client, Extension, Guild, InteractionType, Modal, OptionType, SlashCommandOption
from interactions import SlashContext, ModalContext

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def macro():
    return "Macro Test"


@pytest.fixture
def macros(client):
    return Macros(client)

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
def slash_context_withOptions(client):
    options = [
        interactions.SlashCommandOption(
            name="macro",
            description="macro para editar",
            type=interactions.OptionType.STRING,
            required=True,
        )
    ]
        
    slash_context = SlashContext.from_dict(client, {
        "id":1234,
        "type":InteractionType.APPLICATION_COMMAND,
        "channel_id": 123412, 
        "guild_id": 123123, 
        "locale":"pt-BR", 
        "token":"dummy",
        "data": {"id":99898, "name":"name"},
        "user":{"id":123123, "username":"fulano", "avatar": "", "discriminator":123123},
        "options": options
        })
    return slash_context


@pytest.fixture
def send_modal():
    async def send_modal(modal):
        return None
    return send_modal

@pytest.fixture
def wait_for_modal(client):
    async def wait_for_modal(modal):
        ctx = ModalContext(client)
        ctx.responses = dict.fromkeys(["macro-title", "macro-text"], "Valor Padrão")
        return ctx
    return wait_for_modal

@pytest.fixture
def modal_context(client):
    modal_context = ModalContext(client)
    modal_context.responses = {"macro-title": "Valor Padrão", "macro-text": "Valor Padrão"}
    return modal_context

@pytest.mark.asyncio
async def test_macro_add(mocker, macros, client, slash_context, wait_for_modal, send_modal):
    macro_text = "Valor Padrão"
    macro_title = "Valor Padrão"
    guild_id = 123123
    mock_macro_add = mocker.patch("extensions.macro.Macros.macro_insert")
    mock_modal_ctx_send = mocker.patch("interactions.ModalContext.send")
    client.wait_for_modal = wait_for_modal
    slash_context.send_modal = send_modal
    await macros.macro_add(slash_context)
    mock_macro_add.assert_called_once_with(guild_id, macro_title, macro_text)
    mock_modal_ctx_send.assert_called_once_with(f"Macro **{macro_title}** adicionada.")



@pytest.fixture
def macro_repository_mock():
    # Create a MagicMock instance to mock the MacroRepository class
    macro_repository_mock = MagicMock()
    macro_repository_mock.update_macro = MagicMock()
    macro_repository_mock.delete_macro = MagicMock()

    return macro_repository_mock


@pytest.mark.asyncio
async def test_macro_edit(mocker, macros, client, slash_context_withOptions, wait_for_modal, send_modal, macro_repository_mock, macro):
    mock_modal_ctx_send = mocker.patch("interactions.ModalContext.send")
    client.wait_for_modal = wait_for_modal
    macros.macro_repository = macro_repository_mock
    slash_context_withOptions.send_modal = send_modal
    await macros.macro_edit(slash_context_withOptions, macro)
    mock_modal_ctx_send.assert_called_once_with(f"Macro **{macro}** editada!")


@pytest.mark.asyncio
async def test_macro_delete(mocker, macros, client, slash_context, macro_repository_mock, slash_context_withOptions, macro):
    macro_text = "Valor Padrão"
    macro_title = "Valor Padrão"
    guild_id = 123123
    mock_modal_ctx_send = mocker.patch("interactions.ModalContext.send")
    await macros.macro_delete(slash_context_withOptions, macro)
    macros.macro_repository = macro_repository_mock
    mock_modal_ctx_send.assert_called_once_with(f"Macro **{macro_title}** adicionada.")