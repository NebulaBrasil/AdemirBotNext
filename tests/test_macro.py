from unittest.mock import AsyncMock, MagicMock
import uuid
from bson import Binary, UuidRepresentation
import pytest
from entities.macro_entity import Macro
from extensions.macro import Macros
from interactions import Client, Extension, Guild, InteractionType, Modal, OptionType, SlashCommandOption
from interactions import SlashContext, ModalContext

@pytest.fixture
def client():
    return Client()

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
def modal_context(client):
    modal_context = ModalContext(client)
    modal_context.responses = {"macro-title": "Valor Padrão", "macro-text": "Valor Padrão"}
    return modal_context

@pytest.mark.asyncio
async def test_macro_add_success(mocker, macros, modal_context):
    macro_text = "Valor Padrão"
    macro_title = "Valor Padrão"
    guild_id = 123123
    
    slash_context = mocker.MagicMock()
    slash_context.guild_id = guild_id
    slash_context.send_modal = mocker.AsyncMock()
    slash_context.bot = mocker.MagicMock()
    slash_context.bot.wait_for_modal = mocker.AsyncMock()
    slash_context.bot.wait_for_modal.return_value = modal_context

    modal_context.responses = {
        "macro-title": macro_title,
        "macro-text": macro_text
    }
    modal_context.send = mocker.AsyncMock()
    modal_context.defer = mocker.AsyncMock()
    modal_context.id = "mock_id" 
    modal_context.token = "mock_token"
    mocker.patch.object(macros, 'macro_insert', return_value=True)

    await macros.macro_add(slash_context)

    macros.macro_insert.assert_called_once_with(guild_id, macro_title, macro_text)

    modal_context.send.assert_called_once_with(f"Macro **{macro_title}** adicionada.")

@pytest.mark.asyncio
async def test_macro_add_failure(mocker, macros, modal_context):
    macro_text = "Valor Padrão"
    macro_title = "Valor Padrão"
    guild_id = 123123

    slash_context = mocker.MagicMock()
    slash_context.guild_id = guild_id
    slash_context.send_modal = mocker.AsyncMock()
    slash_context.bot = mocker.MagicMock()
    slash_context.bot.wait_for_modal = mocker.AsyncMock()
    slash_context.bot.wait_for_modal.return_value = modal_context

    modal_context.responses = {
        "macro-title": macro_title,
        "macro-text": macro_text
    }
    modal_context.send = mocker.AsyncMock()
    modal_context.defer = mocker.AsyncMock()
    modal_context.id = "mock_id"
    modal_context.token = "mock_token"
    mocker.patch.object(macros, 'macro_insert', return_value=False)

    await macros.macro_add(slash_context)
    modal_context.send.assert_called_once_with(f"Macro **{macro_title}** já existe!")

@pytest.mark.asyncio
async def test_macro_edit_success(mocker, macros):
    macro_title = "Valor Padrão"
    macro_text = "Valor Editado"
    guild_id = 123123

    slash_option_mock = mocker.MagicMock()
    slash_option_mock.value = macro_title  # Mock do SlashOption

    slash_context = mocker.MagicMock()
    slash_context.guild_id = guild_id
    slash_context.send_modal = mocker.AsyncMock()
    slash_context.bot = mocker.MagicMock()
    slash_context.bot.wait_for_modal = mocker.AsyncMock()
    slash_context.bot.wait_for_modal.return_value = modal_context
    slash_context.args = [macro_title]
    slash_context.kwargs = {"macro": macro_title}

    modal_context.responses = {
        "macro-text": macro_text
    }
    modal_context.send = mocker.AsyncMock()
    modal_context.defer = mocker.AsyncMock()
    modal_context.id = "mock_id"
    modal_context.token = "mock_token"

    macro_value = Macro(macro_id=uuid.uuid4(), guild_id=guild_id, title=macro_title, text="Valor Padrão")
    mocker.patch.object(macros, 'get_macro_by_title_and_guild_id', return_value=macro_value)
    mocker.patch.object(macros, 'macro_insert', return_value=True)
    mocker.patch.object(macros, 'update_guild_macros', return_value=True)

    await macros.macro_edit(slash_context)

@pytest.mark.asyncio
async def test_macro_edit_failure(mocker, macros):
    macro_title = "Macro Não Existente"
    guild_id = 123123

    slash_context = mocker.MagicMock()
    slash_context.guild_id = guild_id
    slash_context.send = mocker.AsyncMock()
    slash_context.bot = mocker.MagicMock()
    slash_context.args = [macro_title]
    slash_context.kwargs = {"macro": macro_title}

    mocker.patch.object(macros, 'get_macro_by_title_and_guild_id', return_value=None)
    await macros.macro_edit(slash_context)
    slash_context.send.assert_awaited_with(f"A macro **{macro_title}** não existe neste servidor!")

@pytest.mark.asyncio
async def test_macro_delete_success(mocker, macros):
    macro_title = "Macro para Deletar"
    guild_id = 123123

    slash_context = mocker.MagicMock()
    slash_context.guild_id = guild_id
    slash_context.send = mocker.AsyncMock()
    slash_context.defer = mocker.AsyncMock() 
    slash_context.bot = mocker.MagicMock()
    slash_context.args = [macro_title]
    slash_context.kwargs = {"macro": macro_title}
    my_uuid = uuid.uuid4()
    bson_uuid = Binary.from_uuid(my_uuid, uuid_representation=UuidRepresentation.STANDARD)

    macro = Macro(macro_id=bson_uuid, guild_id=guild_id, title=macro_title, text="Valor Padrão")
    mocker.patch.object(Macros, 'get_macro_by_title_and_guild_id', return_value=macro)
    macro_repository_mock = mocker.MagicMock()
    mocker.patch('repository.macro_repository.MacroRepository', return_value=macro_repository_mock)
    mocker.patch.object(macros, 'update_guild_macros')
    await macros.macro_delete(slash_context)
    slash_context.send.assert_awaited_with(f"A macro **{macro_title}** foi deletada!")

@pytest.mark.asyncio
async def test_macro_delete_not_found(mocker, macros):
    macro_title = "Macro inexistente"
    guild_id = 123123

    slash_context = mocker.MagicMock()
    slash_context.guild_id = guild_id
    slash_context.send = mocker.AsyncMock()
    slash_context.defer = mocker.AsyncMock()
    slash_context.bot = mocker.MagicMock()
    slash_context.args = [macro_title]
    slash_context.kwargs = {"macro": macro_title}

    # Simula que não há uma macro correspondente para deletar
    mocker.patch.object(Macros, 'get_macro_by_title_and_guild_id', return_value=None)

    macro_repository_mock = mocker.MagicMock()
    mocker.patch('repository.macro_repository.MacroRepository', return_value=macro_repository_mock)
    mocker.patch.object(macros, 'update_guild_macros')

    await macros.macro_delete(slash_context)

    slash_context.send.assert_awaited_with(f"A macro **{macro_title}** não existe neste servidor!")