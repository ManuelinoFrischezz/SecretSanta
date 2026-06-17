import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

PARTICIPANTS_FILE = os.path.join(
    BASE_DIR,
    "config",
    "participants.json",
)

ASSIGNMENTS_DIR = os.path.join(
    BASE_DIR,
    "config",
    "assignments",
)


def load_json(filepath: str):

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filepath: str, data) -> None:

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False,
        )
