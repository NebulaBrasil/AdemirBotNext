import interactions
from interactions import Extension, OptionType, Role, slash_option
from repository.ademir_cfg_repository import AdemirCfgRepository

class ConfigManage(Extension):
    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client        
        self.repo = AdemirCfgRepository()

    @interactions.slash_command(
        name="config-cargo-ademir", 
        description="Configurar cargo que pode falar com o Ademir.",
        default_member_permissions=interactions.Permissions.ADMINISTRATOR
    )
    @slash_option(
        name="cargo",
        description="Cargo permitido falar com o Ademir",
        required=True,
        opt_type=OptionType.ROLE
    )
    async def configure_conversation_role(self, ctx: interactions.SlashContext, cargo: Role):
        await ctx.defer()
        self.repo.set_guild_conversation_role(ctx.guild_id, cargo.id)
        await ctx.send(f"Cargo {cargo.mention} permitido para o Ademir configurado.", ephemeral=True)

def setup(client):
    ConfigManage(client)