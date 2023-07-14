import interactions
import openai
import config

openai.api_key = config.OPENAPI_TOKEN

class GptAssistant(interactions.Extension):
    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
    
    @interactions.slash_command("hello", description="Say hello!")
    async def hello(self, ctx: interactions.SlashContext):
        await ctx.send("This command is ran inside an Extension")

def setup(client):
    GptAssistant(client)