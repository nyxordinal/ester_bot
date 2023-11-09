import os
import random
from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Client, utils


class Scheduler:
    client: Client
    last_sent_date_morning: datetime
    last_sent_date_evening: datetime
    user_id: str
    morning_sentences = [
        "Pagi, sayang! Bangun, yuk, ada dunia yang menunggu kita!",
        "Halo, cinta! Selamat pagi. Semangat buat hari ini, ya!",
        "Pagi yang cerah kaya senyummu. Yuk, semangat jalani hari!",
        "Selamat pagi, pacar terhebat di dunia ini. Semoga hari ini penuh keberuntungan!",
        "Pagi yang indah kayak wajahmu. Selamat pagi, my sunshine!",
        "Bangun, bangun, bangun! Pagi ini spesial karena kita bersama.",
        "Halo, kesayangan hati! Pagi ini, mari kita buat hari ini lebih baik dari kemarin.",
        "Selamat pagi, pacar tercinta. Semoga hari ini penuh tawa dan kebahagiaan.",
        "Pagi, beb! Semangat untuk hari yang penuh petualangan!",
        "Pagi ini aku ngirim energi positif buatmu. Selamat pagi, my love!",
        "Semoga hari ini membawa banyak kebahagiaan dan sukses. Selamat pagi, sayang!",
        "Hari ini adalah kesempatan baru. Ayo jalani dengan semangat! Selamat pagi, pacarku.",
        "Bangun dengan senyuman karena kamu membuat dunia ini lebih indah. Selamat pagi, cinta!",
        "Pagi ini, mari bersyukur untuk semua kebahagiaan yang kita miliki. Selamat pagi, sayang!",
        "Selamat pagi, kesayangan hati. Mari kita membuat hari ini luar biasa!",
        "Hari ini adalah canvas kosong. Ayo warnai dengan kebahagiaan dan cinta. Selamat pagi, pacar tercinta!",
        "Pagi yang cerah ini memanggil kita untuk menjalani petualangan baru. Selamat pagi, my dear!",
        "Semoga hari ini penuh dengan keberuntungan dan kebahagiaan. Selamat pagi, sayang!",
        "Bangun dengan semangat karena kamu punya kekuatan untuk membuat hari ini luar biasa. Selamat pagi, cinta!",
        "Pagi ini, jangan lupa tersenyum. Senyummu adalah sinar matahari di hari kelabu. Selamat pagi, pacar terbaik!",
    ]
    evening_sentences = [
        "Malam, sayang! Semoga bintang-bintangnya bikin kita ngerasa di film romantis.",
        "Malam ini, cuekin aja semua masalah. Selamat tidur yang nyenyak, ya!",
        "Waktunya recharge tenaga. Selamat malam, pacar terhebat di dunia!",
        "Bobo yuk, beb. Biar besok energinya kembali full. Selamat malam!",
        "Selamat malam, kesayangan hati. Semoga tidurmu enak kayak guling baru.",
        "Ayo tidur, nanti kita ketemu lagi di dunia mimpi yang penuh petualangan.",
        "Pesan tidur untukmu: selamat malam, pacar terbaik di muka bumi!",
        "Malam ini, istirahat yang bener ya. Besok kita tackle masalah lagi. Sweet dreams, sayang!",
        "Waktunya istirahat. Selamat malam, my love. Sweet dreams!",
        "Malam ini, kirimin ciuman virtual buat kamu. Selamat tidur, ya, sayang!",
        "Tidur dengan nyenyak dan bermimpi indah, pacarku. Sampai jumpa di pagi yang cerah!",
        "Dalam mimpiku, kita selalu bareng. Selamat malam, kesayangan hati.",
        "Waktu untuk meresapi kebahagiaan dalam mimpi. Selamat malam, sayang!",
        "Malam ini, terima kasih untuk semua kenangan indah. Selamat tidur, pacarku tercinta.",
        "Bobo yang nyaman, ya, sayang. Esok hari ada banyak kesempatan baru nungguin kita.",
        "Malam ini, biar hati kita tenang. Selamat tidur dan mimpi indah, beb!",
        "Pesan singkat sebelum tidur: aku cinta kamu lebih dari sekadar kata-kata. Selamat malam, pacar terbaik.",
        "Selamat malam, kesayangan hati. Semoga tidurmu penuh ketenangan.",
        "Waktunya melepaskan beban dan masuk ke dunia mimpi. Selamat malam, sayang.",
        "Malam yang tenang ini membawa pesan cinta buat kamu. Selamat tidur, pacarku tercinta.",
    ]

    def __init__(self, client, channel):
        self.client = client
        self.channel = channel
        self.timezone = pytz.timezone("Asia/Jakarta")
        yesterday = datetime.now(self.timezone) - timedelta(days=1)
        self.last_sent_date_morning = yesterday
        self.last_sent_date_evening = yesterday
        self.user_id = os.getenv("USER_ID")

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
        return random.choice(self.morning_sentences)

    def get_evening_text(self) -> str:
        return random.choice(self.evening_sentences)

    async def schedule_func(self):
        current_time = datetime.now(self.timezone)
        current_hour = current_time.hour
        if (8 <= current_hour <= 10) and not self.is_same_date(
            self.last_sent_date_morning, current_time
        ):
            print(
                "send morning message: ", current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
            )
            self.last_sent_date_morning = current_time
            await self.channel.send(self.get_text("MORNING"))
        elif 21 <= current_hour <= 23 and not self.is_same_date(
            self.last_sent_date_evening, current_time
        ):
            print(
                "send evening message: ", current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
            )
            self.last_sent_date_evening = current_time
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
        os.getenv("CRON_EXPRESSION")
        scheduler.add_job(
            self.schedule_func, CronTrigger.from_crontab(os.getenv("CRON_EXPRESSION"))
        )
        scheduler.start()
