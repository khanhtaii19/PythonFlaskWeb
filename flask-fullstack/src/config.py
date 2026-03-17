import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET: str = os.getenv('JWT_SECRET', 'secret_key')
JWT_EXPIRE_DAYS: int = int(os.getenv('JWT_EXPIRE_DAYS', 7))
ADMIN_EMAIL: str = os.getenv('ADMIN_EMAIL', '').strip().lower()
ADMIN_PASSWORD: str = os.getenv('ADMIN_PASSWORD', '')
CORS_ORIGIN: str = os.getenv('CORS_ORIGIN', 'http://localhost:5173')
