import json
import random

SENTENCES_MORNING_FILE = "sentences_morning.json"
SENTENCES_EVENING_FILE = "sentences_evening.json"
sentences_morning = []
sentences_evening = []

with open(SENTENCES_MORNING_FILE, "r") as file:
    try:
        sentences_morning = json.load(file)
    except json.JSONDecodeError:
        print("Error decoding morning JSON.")
with open(SENTENCES_EVENING_FILE, "r") as file:
    try:
        sentences_evening = json.load(file)
    except json.JSONDecodeError:
        print("Error decoding evening JSON.")


def get_text(period) -> str:
    if period == "MORNING":
        # return f"{get_morning_text()} <@{user_id}>"
        return f"{get_morning_text()} @everyone"
    elif period == "EVENING":
        # return f"{get_evening_text()} <@{user_id}>"
        return f"{get_evening_text()} @everyone"
    else:
        return "Hi!"


def get_morning_text() -> str:
    return random.choice(sentences_morning)


def get_evening_text() -> str:
    return random.choice(sentences_evening)
