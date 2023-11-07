import os

import discord
from dotenv import load_dotenv

from scheduler import Scheduler

load_dotenv()
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"logged in as {client.user.name}")
    channel = client.get_channel(int(os.getenv("CHANNEL_ID")))
    scheduler = Scheduler(client=client, channel=channel)
    scheduler.schedule()


if __name__ == "__main__":
    client.run(os.getenv("DISCORD_TOKEN"))
