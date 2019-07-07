import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
