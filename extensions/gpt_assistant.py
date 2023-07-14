import interactions
import openai
import config

openai.api_key = config.OPENAPI_TOKEN

class GptAssistant(interactions.Extension):
    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
    
    @interactions.listen()
    async def on_message_create(self, message_create: interactions.events.MessageCreate):
        message: interactions.Message = message_create.message        
        if message.client.user.mention in message.content:                
            response = openai.ChatCompletion.create(
                model=config.CHAT_GPT_MODEL,
                messages=[{ "role": "user", "content": str.replace(message.content, message.client.user.mention, config.NOME_BOT) }]
                )
            await message.channel.send(response["choices"][0]["message"]["content"])

    @interactions.slash_command("hello", description="Say hello!")
    async def hello(self, ctx: interactions.SlashContext):
        await ctx.send("This command is ran inside an Extension")

def setup(client):
    GptAssistant(client)