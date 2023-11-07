import os
from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Client


class Scheduler:
    client: Client
    last_sent_date_morning: datetime
    last_sent_date_evening: datetime
    TEXTS = {
        "MORNING": "Selamat pagi sayang, selamat beraktivitas!",
        "EVENING": "Selamat tidur sayang :)",
    }

    def __init__(self, client, channel):
        self.client = client
        self.channel = channel
        self.timezone = pytz.timezone("Asia/Jakarta")
        yesterday = datetime.now(self.timezone) - timedelta(days=1)
        self.last_sent_date_morning = yesterday
        self.last_sent_date_evening = yesterday

    def is_same_date(self, date1, date2):
        return date1.date() == date2.date()

    def get_text(self, period) -> str:
        # for more variations, you can make list of texts and pick random
        return self.TEXTS.get(period, "Jangan lupa bahagia")

    async def schedule_func(self):
        current_time = datetime.now(self.timezone)
        print(
            "job triggered: ", current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
        )  # safe to remove
        current_hour = current_time.hour
        if (0 <= current_hour <= 1) and not self.is_same_date(
            self.last_sent_date_morning, current_time
        ):
            print("send morning message")  # safe to remove
            self.last_sent_date_morning = current_time
            await self.channel.send(self.get_text("MORNING"))
        elif 21 <= current_hour <= 22 and not self.is_same_date(
            self.last_sent_date_evening, current_time
        ):
            print("send evening message")  # safe to remove
            self.last_sent_date_evening = current_time
            await self.channel.send(self.get_text("EVENING"))
        else:
            print("skip")  # safe to remove

    def schedule(self):
        print("init scheduler")
        job_defaults = {
            "coalesce": True,
            "max_instances": 5,
            "misfire_grace_time": 15,
            "replace_existing": True,
        }
        scheduler = AsyncIOScheduler(job_defaults=job_defaults)
        os.getenv("CRON_EXPRESSION")
        scheduler.add_job(
            self.schedule_func, CronTrigger.from_crontab(os.getenv("CRON_EXPRESSION"))
        )
        scheduler.start()
