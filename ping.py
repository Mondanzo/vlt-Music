# This is a stupid file for a friend (but you can start coding with it!
# This file is not licensed under MIT!

import discord
client = discord.Client()
async def on_message(message):
    if message.content.startswith("ping"):
        await client.send_message(message.channel, "Ping")
client.run("your token")
