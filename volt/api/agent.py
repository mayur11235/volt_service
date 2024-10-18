import json
from fastapi import APIRouter, Request, HTTPException, Header
from volt.services.agent_api_service import AgentAPIService

router = APIRouter()

agent_service = AgentAPIService()

@router.post("/agent")
async def chat_completion(request: Request, github_public_key_signature: str = Header(None)):
    body = await request.body()

    is_valid = agent_service.valid_payload(body, github_public_key_signature)
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid payload signature")

    try:
        request_data = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    return await agent_service.generate_completion(request_data)