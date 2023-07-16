from bson.json_util import dumps
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
                messages=[{ "role": "user", "content": str.replace(message.content, message.client.user.mention, config.BOT_NAME) }]
                )
            await message.channel.send(response["choices"][0]["message"]["content"])

def setup(client):
    GptAssistant(client)