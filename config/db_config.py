from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class DBConfig:
    host: str = os.getenv('DB_HOST')
    user: str = os.getenv('DB_USER')
    password: str = os.getenv('DB_PASSWORD')
    database: str = os.getenv('DB_NAME')
