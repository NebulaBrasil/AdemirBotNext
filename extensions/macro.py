import uuid
import interactions
from interactions import Client, Extension, Guild, Modal, ModalContext, ParagraphText, ShortText
import openai
import config
from repository.macro_repository import MacroRepository
from entities.macro_entity import Macro

import logging

logger = logging.getLogger(__name__)

openai.api_key = config.OPENAPI_TOKEN

class Macros(Extension):
    def __init__(self, client: Client) -> None:
        self.client: Client = client

    def macro_insert(self, guild_id: int, macro_title: str, macro_text: str):
        macro_repository = MacroRepository()
        macro = macro_repository.get_macro_by_title(macro_title)
        if macro is None:
            new_macro = Macro(guild_id=guild_id, title=macro_title, text=macro_text)
            macro_repository.create_macro(new_macro)
            return True
        else:
            return False

    @interactions.slash_command(
        name="macro-add", 
        description="Adiciona uma macro.",
        default_member_permissions=interactions.Permissions.ADMINISTRATOR
    )
    async def macro_add(self, ctx: interactions.SlashContext):
        modal = Modal(
            ShortText(label="Nome da Macro", custom_id="macro-title", placeholder="Insira um título", required=True),
            ParagraphText(label="Texto da Macro", custom_id="macro-text", placeholder="Insira uma descrição", required=True),
            title="Adicionar Macro",
            custom_id="macro_add_form"
        )
        await ctx.send_modal(modal)        
        modal_ctx: ModalContext = await ctx.bot.wait_for_modal(modal)
        macro_title = modal_ctx.responses["macro-title"]
        macro_text = modal_ctx.responses["macro-text"]
        #member_ids = self.split_and_parse_member_ids(member_str)
        macro_created = self.macro_insert(ctx.guild_id, macro_title, macro_text)
        if macro_created:
            await modal_ctx.send(f"Macro **{macro_title}** adicionada.")
        else:
            await modal_ctx.send(f"Macro **{macro_title}** já existe!")