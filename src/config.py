import os
from dotenv import load_dotenv


load_dotenv()
user = os.getenv("BD_USER")
password = os.getenv("BD_PASSWORD")
host = os.getenv("BD_HOST")
db_port = os.getenv("BD_PORT")


def DATA_BASE_URL():
    return f"postgresql+asyncpg://{user}:{password}@{host}:{db_port}"
