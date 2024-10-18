import os
from dotenv import load_dotenv

load_dotenv()
load_dotenv(os.path.expanduser("~/.env"))
class Config:
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    FQDN = os.getenv("FQDN")
    OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")