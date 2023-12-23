from dotenv import load_dotenv
from environs import Env

load_dotenv()
env = Env()


class Settings:
    MODEL_URL = env.str("MODEL_URL")
    PATH_TO_SWEAR_WORDS = env.str("PATH_TO_SWEAR_WORDS")
    TOKEN = env.str("TOKEN")

    # http
    MAX_CONNECTIONS = env.int("MAX_CONNECTIONS")
    MAX_KEEPALIVE_CONNECTIONS = env.int("MAX_KEEPALIVE_CONNECTIONS")
    KEEPALIVE_EXPIRY = env.int("KEEPALIVE_EXPIRY")
    HTTP_TIMEOUT = env.int("HTTP_TIMEOUT")
