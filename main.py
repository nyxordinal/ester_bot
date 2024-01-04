import os

from dotenv import load_dotenv
from interactions import (
    Client,
    Intents,
    IntervalTrigger,
    SlashContext,
    Task,
    listen,
    slash_command,
)

from db import (
    DB_FILE_JSON,
    LAST_SENT_DATE_EVENING,
    LAST_SENT_DATE_MORNING,
    USER_IDS,
    FileDB,
)
from message import get_text
from util import get_current_time, get_timezone, get_yesterday_date, is_same_date

load_dotenv()

channel_id = os.getenv("CHANNEL_ID")
admin_id = os.getenv("ADMIN_ID")
morning_hour_start = int(os.getenv("MORNING_HOUR_START"))
morning_hour_end = int(os.getenv("MORNING_HOUR_END"))
evening_hour_start = int(os.getenv("EVENING_HOUR_START"))
evening_hour_end = int(os.getenv("EVENING_HOUR_END"))
timezone = get_timezone("Asia/Jakarta")

bot = Client(intents=Intents.DEFAULT)
db = FileDB(DB_FILE_JSON)


def setup_db():
    yesterday = get_yesterday_date(timezone=timezone)
    db.set(LAST_SENT_DATE_MORNING, yesterday)
    db.set(LAST_SENT_DATE_EVENING, yesterday)
    if db.get(USER_IDS) == None:
        db.set(USER_IDS, [])


@listen()
async def on_ready():
    print(f"logged in as {bot.owner}")
    print(f"channel_id: {channel_id}")
    print(f"admin_id: {admin_id}")
    setup_db()


@slash_command(name="bot_start", description="Start the bot to sending message")
async def bot_start(ctx: SlashContext):
    if str(ctx.author.id) == admin_id:
        await ctx.send("Starting bot")
        send_greetings_message.start()
    else:
        await ctx.send("You don't have access to run this command")


@slash_command(name="bot_stop", description="Stop the bot from sending message")
async def bot_stop(ctx: SlashContext):
    if str(ctx.author.id) == admin_id:
        await ctx.send("Stopping bot")
        send_greetings_message.stop()
    else:
        await ctx.send("You don't have access to run this command")


@slash_command(
    name="mention_me",
    description="Add yourself to be mentioned in the message by the bot",
)
async def mention_me(ctx: SlashContext):
    user_ids = db.get(USER_IDS)
    if ctx.author.id in user_ids:
        await ctx.send("No worries, you are on the list")
    else:
        print(
            f"adding user to the mention list, name: {ctx.author.username}, id: {ctx.author.id}"
        )
        user_ids.append(ctx.author.id)
        db.set(USER_IDS, user_ids)
        await ctx.send("You are on the list now!")


@slash_command(
    name="unmention_me",
    description="Remove yourself from being mentioned by the bot",
)
async def unmention_me(ctx: SlashContext):
    user_ids = db.get(USER_IDS)
    if ctx.author.id in user_ids:
        print(
            f"removing user from mention list, name: {ctx.author.username}, id: {ctx.author.id}"
        )
        user_ids.remove(ctx.author.id)
        db.set(USER_IDS, user_ids)
        await ctx.send("You are no longer in the list")
    else:
        await ctx.send("Got it, you are not on the list")


@Task.create(IntervalTrigger(minutes=30))
async def send_greetings_message():
    current_time = get_current_time(timezone=timezone)
    current_hour = current_time.hour

    channel = bot.get_channel(channel_id=int(channel_id))

    if channel:
        if not is_same_date(db.get(LAST_SENT_DATE_MORNING), current_time) and (
            morning_hour_start <= current_hour <= morning_hour_end
        ):
            print(
                "send morning message: ", current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
            )
            db.set(LAST_SENT_DATE_MORNING, current_time)
            await channel.send(get_message_with_mentions(get_text("MORNING")))
        elif not is_same_date(db.get(LAST_SENT_DATE_EVENING), current_time) and (
            evening_hour_start <= current_hour <= evening_hour_end
        ):
            print(
                "send evening message: ", current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
            )
            db.set(LAST_SENT_DATE_EVENING, current_time)
            await channel.send(get_message_with_mentions(get_text("EVENING")))
    else:
        print("invalid channel ID")


def get_message_with_mentions(msg: str):
    user_ids = db.get(USER_IDS)
    user_mentions = " ".join([f"<@{user_id}>" for user_id in user_ids])
    return f"{msg} {user_mentions}"


# start the bot
token = os.getenv("DISCORD_TOKEN")
if token is not None and token != "":
    bot.start(os.getenv("DISCORD_TOKEN"))
else:
    print("please set your discord token")
