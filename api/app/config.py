import os

DATABASE_URL = os.environ.get("DATABASE_URL")
REDIS_URL = os.environ.get("REDIS_URL")
STARTUP_DELAY_SECONDS = int(os.environ.get("STARTUP_DELAY_SECONDS", 0))
CHAOS_MODE = os.environ.get("CHAOS_MODE", '')


