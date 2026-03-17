import os
from dotenv import load_dotenv

# load file .env
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_EXPIRE_DAYS = int(os.getenv("JWT_EXPIRE_DAYS", 7))

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")