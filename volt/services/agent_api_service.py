import requests
import base64
from fastapi import HTTPException , Request
from fastapi.responses import StreamingResponse
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from volt.services.lang_service import LangService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentAPIService:
    def __init__(self):
        self.public_key = self.fetch_public_key()
    
    def fetch_public_key(self):
        url = "https://api.github.com/meta/public_keys/copilot_api"
        response = requests.get(url)
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Failed to fetch public key: {response.status}")
        
        data = response.json()
        current_key = next((pk['key'] for pk in data['public_keys'] if pk['is_current']), None)
        
        if not current_key:
            raise HTTPException(status_code=500, detail="No current public key found")

        return current_key

    def valid_payload(self, payload, signature):
        signature = base64.b64decode(signature)        
        public_key = serialization.load_pem_public_key(self.public_key.encode('utf-8'), default_backend())

        try:
            public_key.verify(signature,payload,ec.ECDSA(hashes.SHA256()))
            return True
        except Exception as e:
            logger.error(str(e))
            return False        

    async def generate_completion(self, request_data:Request):
        return StreamingResponse(LangService.model_response(request_data), media_type="text/event-stream")
    