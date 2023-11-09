import os
import sys

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
    channel_id = os.getenv("CHANNEL_ID")
    print(f"channel_id: {channel_id}")
    channel = client.get_channel(int(channel_id))
    scheduler = Scheduler(client=client, channel=channel)
    scheduler.schedule()


if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if token != None and token != "":
        client.run(token=token)
    else:
        print("please set your discord token")
        sys.exit()
