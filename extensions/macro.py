import uuid
from discord_typings import SelectMenuComponentData, SelectMenuOptionData
import interactions
from interactions import Client, Extension, Guild, Modal, ModalContext, ParagraphText, ShortText, StringSelectMenu, StringSelectOption
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

    def get_macro_by_title_and_guild_id(self, macro_title: str, guild_id: int):
        macro_repository = MacroRepository()
        return macro_repository.get_macro_by_title_and_guild_id(macro_title, guild_id)

    def macro_insert(self, guild_id: int, macro_title: str, macro_text: str):
        macro = self.get_macro_by_title_and_guild_id(macro_title, guild_id)
        if macro is None:
            macro_repository = MacroRepository()
            new_macro = Macro(macro_id=uuid.uuid4(),guild_id=guild_id, title=macro_title, text=macro_text)
            macro_repository.create_macro(new_macro)
            return True
        else:
            return False
    
    def trim_text(self, text):
        if len(text) > 900:
            return text[:850] + "..."
        return text
        
    def find_all_macros(self, guild_id: int):
        macro_repository = MacroRepository()
        all_macros = list(macro_repository.find_all(guild_id))
        return True
    
    @interactions.slash_command(
        name="macro-add", 
        description="Adiciona uma macro.",
        default_member_permissions=interactions.Permissions.ADMINISTRATOR
    )
    async def macro_add(self, ctx: interactions.SlashContext):
        modal = Modal(
            ShortText(label="Nome da Macro", custom_id="macro-title", placeholder="Insira um título", required=True),
            ParagraphText(label="Texto da Macro", custom_id="macro-text", placeholder="Insira uma descrição", required=True, min_length=1, max_length=2000),
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

    @interactions.slash_command(
        name="macro-edit", 
        description="Edita uma macro.",
        default_member_permissions=interactions.Permissions.ADMINISTRATOR,
        options=[
            interactions.SlashCommandOption(
                name="macro",
                description="macro para editar",
                type=interactions.OptionType.STRING,
                required=True,
            )
        ],
    )
    async def macro_edit(self, ctx: interactions.SlashContext, macro: str):
        find_macro = self.get_macro_by_title_and_guild_id(macro, ctx.guild_id)
        if find_macro is None:
            await ctx.send(f"A macro **{macro}** não existe neste servidor!")
        else:
            macro_repository = MacroRepository()
            modal = Modal(
                ParagraphText(label="Texto da Macro", custom_id="macro-text", placeholder="Edite o texto da macro", value=find_macro.text, required=True, min_length=1, max_length=2000),
                title="Edite a Macro",
                custom_id="macro_edit_form"
            )
            await ctx.send_modal(modal)
            modal_ctx: ModalContext = await ctx.bot.wait_for_modal(modal)

            macro_title = modal_ctx.responses["macro-title"].capitalize
            macro_new_text = modal_ctx.responses["macro-text"]
            old_macro_text = find_macro.text
            find_macro.text = macro_new_text
            macro_repository.update_macro(find_macro.macro_id, find_macro)

            macro_formated_old_text = self.trim_text(old_macro_text)
            macro_formated_new_text = self.trim_text(find_macro.text)

            mensagem = f"```ansi\n\u001b[2;37mMACRO {macro_title} EDITADA!\n\u001b[0m\u001b[2;31m\u001b[1;31m• ANTES:\n\u001b[0m\u001b[2;31m\u001b[0m{macro_formated_old_text}\n\u001b[2;34m\u001b[1;34m\u001b[0m\u001b[2;34m\u001b[1;34m• DEPOIS:\n\u001b[0m\u001b[2;34m\u001b[0m{macro_formated_new_text}```"
            await modal_ctx.send(mensagem)
    
    @interactions.slash_command(
        name="macro-delete", 
        description="Remove uma macro.",
        default_member_permissions=interactions.Permissions.ADMINISTRATOR,
        options=[
            interactions.SlashCommandOption(
                name="macro",
                description="macro para remover",
                type=interactions.OptionType.STRING,
                required=True,
            )
        ],
    )
    async def macro_delete(self, ctx: interactions.SlashContext, macro: str):
        find_macro = self.get_macro_by_title_and_guild_id(macro, ctx.guild_id)
        if find_macro is None:
            await ctx.send(f"A macro **{macro}** não existe neste servidor!")
        else:
            macro_repository = MacroRepository()
            macro_repository.delete_macro(find_macro.macro_id)
            await ctx.send(f"A macro **{macro}** foi deletada!")
