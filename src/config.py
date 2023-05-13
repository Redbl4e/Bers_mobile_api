from pathlib import Path

from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).parent.parent


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

SECRET_AUTH = os.getenv("SECRET_AUTH")
YANDEX_GEOCODER_API_KEY = os.getenv("YANDEX_GEOCODER_API_KEY")

MEDIA_PATH = BASE_DIR / "media/"
POSTS_PATH = MEDIA_PATH / "posts/"
