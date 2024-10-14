from os import getenv
from dotenv import load_dotenv

load_dotenv()

DB_URL = str(getenv("DB_URL"))
