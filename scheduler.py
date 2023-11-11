import json
import os
import random
from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Client

from db import DB_FILE_JSON, LAST_SENT_DATE_EVENING, LAST_SENT_DATE_MORNING, FileDB

SENTENCES_MORNING_FILE = "sentences_morning.json"
SENTENCES_EVENING_FILE = "sentences_evening.json"


class Scheduler:
    client: Client
    db: FileDB
    user_id: str
    morning_hour_start: int
    morning_hour_end: int
    evening_hour_start: int
    evening_hour_end: int
    sentences_morning: []
    sentences_evening = []

    def __init__(self, client, channel):
        self.client = client
        self.channel = channel
        self.db = FileDB(DB_FILE_JSON)
        self.user_id = os.getenv("USER_ID")
        self.morning_hour_start = int(os.getenv("MORNING_HOUR_START"))
        self.morning_hour_end = int(os.getenv("MORNING_HOUR_END"))
        self.evening_hour_start = int(os.getenv("EVENING_HOUR_START"))
        self.evening_hour_end = int(os.getenv("EVENING_HOUR_END"))
        self.timezone = pytz.timezone("Asia/Jakarta")
        yesterday = datetime.now(self.timezone) - timedelta(days=1)
        self.db.set(LAST_SENT_DATE_MORNING, yesterday)
        self.db.set(LAST_SENT_DATE_EVENING, yesterday)
        with open(SENTENCES_MORNING_FILE, "r") as file:
            try:
                self.sentences_morning = json.load(file)
            except json.JSONDecodeError:
                print("Error decoding morning JSON.")
        with open(SENTENCES_EVENING_FILE, "r") as file:
            try:
                self.sentences_evening = json.load(file)
            except json.JSONDecodeError:
                print("Error decoding evening JSON.")

    def is_same_date(self, date1, date2):
        return date1.date() == date2.date()

    def get_text(self, period) -> str:
        if period == "MORNING":
            # return f"{self.get_morning_text()} <@{self.user_id}>"
            return f"{self.get_morning_text()} @everyone"
        elif period == "EVENING":
            # return f"{self.get_evening_text()} <@{self.user_id}>"
            return f"{self.get_evening_text()} @everyone"
        else:
            return "Hi!"

    def get_morning_text(self) -> str:
        return random.choice(self.sentences_morning)

    def get_evening_text(self) -> str:
        return random.choice(self.sentences_evening)

    async def schedule_func(self):
        current_time = datetime.now(self.timezone)
        current_hour = current_time.hour
        if (
            self.morning_hour_start <= current_hour <= self.morning_hour_end
        ) and not self.is_same_date(self.db.get(LAST_SENT_DATE_MORNING), current_time):
            print(
                "send morning message: ", current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
            )
            self.db.set(LAST_SENT_DATE_MORNING, current_time)
            await self.channel.send(self.get_text("MORNING"))
        elif (
            self.evening_hour_start <= current_hour <= self.evening_hour_end
            and not self.is_same_date(self.db.get(LAST_SENT_DATE_EVENING), current_time)
        ):
            print(
                "send evening message: ", current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
            )
            self.db.get(LAST_SENT_DATE_EVENING, current_time)
            await self.channel.send(self.get_text("EVENING"))

    def schedule(self):
        print("init scheduler")
        job_defaults = {
            "coalesce": True,
            "max_instances": 5,
            "misfire_grace_time": 15,
            "replace_existing": True,
        }
        scheduler = AsyncIOScheduler(job_defaults=job_defaults)
        scheduler.add_job(
            self.schedule_func, CronTrigger.from_crontab(os.getenv("CRON_EXPRESSION"))
        )
        scheduler.start()
