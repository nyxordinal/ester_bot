import os

import discord
from discord.ext import tasks
from dotenv import load_dotenv

from db import DB_FILE_JSON, LAST_SENT_DATE_EVENING, LAST_SENT_DATE_MORNING, FileDB
from message import get_text
from util import get_current_time, get_timezone, get_yesterday_date, is_same_date

load_dotenv()

client = discord.Client(intents=discord.Intents(messages=True, guilds=True))
channel_id = os.getenv("CHANNEL_ID")
user_id = os.getenv("USER_ID")
morning_hour_start = int(os.getenv("MORNING_HOUR_START"))
morning_hour_end = int(os.getenv("MORNING_HOUR_END"))
evening_hour_start = int(os.getenv("EVENING_HOUR_START"))
evening_hour_end = int(os.getenv("EVENING_HOUR_END"))
timezone = get_timezone("Asia/Jakarta")
db = FileDB(DB_FILE_JSON)


def setup_db():
    yesterday = get_yesterday_date(timezone=timezone)
    db.set(LAST_SENT_DATE_MORNING, yesterday)
    db.set(LAST_SENT_DATE_EVENING, yesterday)


@client.event
async def on_ready():
    print(f"logged in as {client.user.name}")
    print(f"channel_id: {channel_id}")
    setup_db()
    send_message.start()


@tasks.loop(minutes=30)
async def send_message():
    current_time = get_current_time(timezone=timezone)
    current_hour = current_time.hour

    channel = client.get_channel(int(channel_id))

    if channel:
        if not is_same_date(db.get(LAST_SENT_DATE_MORNING), current_time) and (
                morning_hour_start <= current_hour <= morning_hour_end
        ):
            print(
                "send morning message: ", current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
            )
            db.set(LAST_SENT_DATE_MORNING, current_time)
            await channel.send(get_text("MORNING"))
        elif not is_same_date(db.get(LAST_SENT_DATE_EVENING), current_time) and (
                evening_hour_start <= current_hour <= evening_hour_end
        ):
            print(
                "send evening message: ", current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
            )
            db.set(LAST_SENT_DATE_EVENING, current_time)
            await channel.send(get_text("EVENING"))
    else:
        print("invalid channel ID")


# start the bot
token = os.getenv("DISCORD_TOKEN")
if token is not None and token != "":
    client.run(token=token)
else:
    print("please set your discord token")
