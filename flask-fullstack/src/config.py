import os
from dotenv import load_dotenv

load_dotenv()

FLASK_ENV: str = os.getenv('FLASK_ENV', 'development').strip().lower()
_jwt_from_env = os.getenv('JWT_SECRET', '').strip()
if _jwt_from_env:
    JWT_SECRET: str = _jwt_from_env
elif FLASK_ENV == 'development':
    JWT_SECRET = 'dev-insecure-secret-change-me'
else:
    raise RuntimeError('JWT_SECRET is required outside development environment')

JWT_EXPIRE_DAYS: int = int(os.getenv('JWT_EXPIRE_DAYS', 7))
ADMIN_EMAIL: str = os.getenv('ADMIN_EMAIL', '').strip().lower()
ADMIN_PASSWORD: str = os.getenv('ADMIN_PASSWORD', '')
CORS_ORIGIN: str = os.getenv('CORS_ORIGIN', 'http://localhost:5173')
