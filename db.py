import json
import os
from datetime import datetime

DB_FILE_JSON = "db.json"
LAST_SENT_DATE_MORNING = "last_sent_date_morning"
LAST_SENT_DATE_EVENING = "last_sent_date_evening"


class FileDB:
    def __init__(self, db_file):
        self.db_file = db_file
        self.data = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as file:
                try:
                    self.data = json.load(file)
                    for key, value in self.data.items():
                        if isinstance(value, str) and self.is_valid_iso_date(value):
                            self.data[key] = datetime.fromisoformat(value)
                except json.JSONDecodeError:
                    print("Error decoding JSON. Initializing empty database.")
                    self.data = {}

    def save_data(self):
        for key, value in self.data.items():
            if isinstance(value, datetime):
                self.data[key] = value.isoformat()
        with open(self.db_file, "w") as file:
            json.dump(self.data, file)

    def set(self, key, value):
        self.data[key] = value
        self.save_data()

    def get(self, key, default=None):
        value = self.data.get(key, default)
        if isinstance(value, str) and self.is_valid_iso_date(value):
            return datetime.fromisoformat(value)
        return value

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self.save_data()

    @staticmethod
    def is_valid_iso_date(date_str):
        try:
            datetime.fromisoformat(date_str)
            return True
        except ValueError:
            return False
