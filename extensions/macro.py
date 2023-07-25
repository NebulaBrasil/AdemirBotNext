from pytz import timezone
import interactions
import datetime
import config
import openai
import uuid
from interactions import Client, Embed, Extension, Guild, Modal, ModalContext, ParagraphText, ShortText, StringSelectMenu, StringSelectOption
from discord_typings import SelectMenuComponentData, SelectMenuOptionData
from repository.macro_repository import MacroRepository
from entities.macro_entity import Macro

import logging

logger = logging.getLogger(__name__)

openai.api_key = config.OPENAPI_TOKEN

class Macros(Extension):
    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.macro_repository = MacroRepository()
        self.guild_macros = {}  # Dict to store macros for guild

    async def update_guild_macros(self, guild_id):
        try:
            self.guild_macros[guild_id] = list(self.macro_repository.find_all(guild_id))
        except Exception as e:
            logger.error(f"Failed to update macros for guild {guild_id}: {e}")
            raise

    @interactions.listen('GUILD_CREATE')
    async def on_guild_create(self, guild: Guild):
        await self.update_guild_macros(guild.id)

    def get_macro_by_title_and_guild_id(self, macro_title: str, guild_id: int):
        try:
            return self.macro_repository.get_macro_by_title_and_guild_id(macro_title, guild_id)
        except Exception as e:
            logger.error(f"Failed to get macro {macro_title} for guild {guild_id}: {e}")
            raise

    def macro_insert(self, guild_id: int, macro_title: str, macro_text: str):
        macro = self.get_macro_by_title_and_guild_id(macro_title, guild_id)
        if macro is None:
            new_macro = Macro(macro_id=uuid.uuid4(),guild_id=guild_id, title=macro_title, text=macro_text)
            try:
                self.macro_repository.create_macro(new_macro)
            except Exception as e:
                logger.error(f"Failed to insert macro {macro_title} for guild {guild_id}: {e}")
                raise
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
        await modal_ctx.defer()
        macro_created = self.macro_insert(ctx.guild_id, macro_title, macro_text)
        if macro_created:
            await self.update_guild_macros(ctx.guild_id)
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
            await modal_ctx.defer()
            macro_new_text = modal_ctx.responses["macro-text"]
            old_macro_text = find_macro.text
            find_macro.text = macro_new_text
            macro_repository.update_macro(find_macro.macro_id, find_macro)

            macro_formated_old_text = self.trim_text(old_macro_text)
            macro_formated_new_text = self.trim_text(find_macro.text)
            embed = Embed(
                title=f"Macro \"{macro}\" editada!",
                color=0x71368a,
                timestamp=datetime.datetime.now(timezone('UTC'))
            )
            macro_formated_old_text = f"```diff\n- {macro_formated_old_text}```"  
            macro_formated_new_text = f"```diff\n+ {macro_formated_new_text}```" 

            embed.add_field(name="Antes:", value=macro_formated_old_text, inline=False)
            embed.add_field(name="Depois:", value=macro_formated_new_text, inline=False)

            await self.update_guild_macros(ctx.guild_id)
            await modal_ctx.send(embed=embed)
    
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
        await ctx.defer()
        find_macro = self.get_macro_by_title_and_guild_id(macro, ctx.guild_id)
        if find_macro is None:
            await ctx.send(f"A macro **{macro}** não existe neste servidor!")
        else:
            macro_repository = MacroRepository()
            macro_repository.delete_macro(find_macro.macro_id)
            await self.update_guild_macros(ctx.guild_id)
            await ctx.send(f"A macro **{macro}** foi deletada!")

    @interactions.listen()
    async def on_message_create(self, message_create: interactions.events.MessageCreate):
        message = message_create.message
        guild_id = message_create.message.channel.guild.id

        if guild_id not in self.guild_macros:
            macro_repository = MacroRepository()
            self.guild_macros[guild_id] = list(macro_repository.find_all(guild_id))

        for macro in self.guild_macros[guild_id]:
            if macro.title.strip() == message.content.strip():
                await message.channel.send(macro.text)
                break  



    @interactions.slash_command(
        name="macro-list", 
        description="Lista todas macros do servidor.",
        default_member_permissions=interactions.Permissions.ADMINISTRATOR
    )
    async def macro_list(self, ctx: interactions.SlashContext):
        guild_id = ctx.guild_id
        if guild_id not in self.guild_macros:
            await self.update_guild_macros(guild_id)
        macros = self.guild_macros.get(guild_id, [])

        if not macros:
            await ctx.send("Ainda não possui macros nesse servidor!")
        else:
            embed = Embed(
                title="Macros do Servidor",
                description="Todas as macros deste servidor:",
                color=0x71368a, 
                timestamp=datetime.datetime.now(timezone('UTC'))
            )

            for macro in macros:
                if macro.text.startswith("http") and macro.text.rsplit('.', 1)[-1] in {'png', 'jpg', 'jpeg', 'gif'}:
                    value = f"[Imagem]({macro.text})"
                else:
                    if len(macro.text) > 1024:
                        value = macro.text[:50] + "..."
                    else:
                        value = macro.text
                embed.add_field(name=macro.title, value=value, inline=False)
            
            await ctx.send(embed=embed)

        
