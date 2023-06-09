from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url
from environs import Env

env = Env()
env.read_env()

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG')
DATABASE_URL = os.getenv('DATABASE_URL')
CSRF_TRUSTED_ORIGINS= os.getenv('CSRF_TRUSTED_ORIGINS').split(' ')
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
print(BASE_DIR)


print(os.environ.get('DATABASE_URL'))

