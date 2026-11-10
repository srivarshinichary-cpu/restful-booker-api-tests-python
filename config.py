"""Central configuration. Any value can be overridden with an environment variable."""
import os

BASE_URL = os.getenv("BASE_URL", "https://restful-booker.herokuapp.com")
USERNAME = os.getenv("API_USERNAME", "admin")
PASSWORD = os.getenv("API_PASSWORD", "password123")
TIMEOUT = int(os.getenv("TIMEOUT_SECONDS", "30"))
MAX_RESPONSE_TIME_MS = int(os.getenv("MAX_RESPONSE_TIME_MS", "10000"))
