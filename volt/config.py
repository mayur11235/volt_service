import os
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.env"))
load_dotenv()

class Config:
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    FQDN = os.getenv("FQDN")
    OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
    sample_chat_response = """
data: {"choices":[{"index":0,"delta":{"content":"Hola"}}]} 
data: {"choices":[{"index":0,"delta":{"content":" World !!"}}]}
data: {"choices":[{"index":0,"delta":{"content":null},"finish_reason":"stop"}]}

data: [DONE]
"""