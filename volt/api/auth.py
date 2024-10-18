from uuid import uuid4
from volt.config import Config
from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Request, HTTPException, Cookie
import logging

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

client_id = Config.CLIENT_ID
client_secret = Config.CLIENT_SECRET
callback_url = Config.FQDN + "/auth/callback"

oauth = OAuth()
oauth.register(
    name='github',
    client_id=client_id,
    client_secret=client_secret,
    authorize_url="https://github.com/login/oauth/authorize",
    access_token_url="https://github.com/login/oauth/access_token",
    client_kwargs={'scope': 'user:email'},
    redirect_uri=callback_url
)

@router.get("/auth/authorization")
async def pre_auth(request: Request):
    state = str(uuid4())
    response = await oauth.github.authorize_redirect(request , state=state)
    response.set_cookie("oauth_state", state, httponly=True, max_age=10*60, secure=True, samesite='lax')
    return response

@router.get("/auth/callback")
async def post_auth(request: Request, oauth_state: str = Cookie(None)):
    query_params = dict(request.query_params)
    state = query_params.get('state')
    logger.info(f"state: {state}")
    logger.info(f"oauth_state: {oauth_state}")
    code = query_params.get('code')

    if state != oauth_state:
        raise HTTPException(status_code=400, detail="Invalid state")

    token = await oauth.github.authorize_access_token(request)
    if not token:
        raise HTTPException(status_code=400, detail="Failed to exchange code for token")

    return {"message": "All done! Please return to the app."}
