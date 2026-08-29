from decouple import config

def main() -> None:
    print("Hello from fastapiauth!")
    
DB_URL = config('DATABASE_URL')
DEBUG = config('DEBUG', cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
TOKEN_EXPIRE_MINUTES = config('TOKEN_EXPIRE_MINUTES', cast=int)
ISSUER = config('ISSUER')
AUDIENCE = config('AUDIENCE')