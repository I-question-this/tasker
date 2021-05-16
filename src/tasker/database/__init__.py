import json
import os

from .database import Database
from .task import Task
from .day import Day


HOME_DIR = os.environ['HOME']
DATA_DIR = os.path.join(HOME_DIR, ".local/tasker")
if not os.path.isdir(DATA_DIR):
    os.mkdir(DATA_DIR)

DATA_PATH = os.path.join(DATA_DIR, "data.json")
if os.path.isfile(DATA_PATH):
    with open(DATA_PATH, 'r') as fin:
        DATABASE = Database.from_dict(json.load(fin))
else:
    DATABASE = Database()


def save_database():
    with open(DATA_PATH, 'w') as fout:
        json.dump(DATABASE.to_dict(), fout, indent=1)
