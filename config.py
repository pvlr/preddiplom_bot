from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class Config:
    bot_token: str
    db_path: str

def load_config() -> Config:
    return Config(
        bot_token = os.getenv("BOT_TOKEN"),
        db_path = os.getenv("DB_PATH")
    )
