import os
import uvicorn
from fastapi import FastAPI
from volt.api import auth, agent
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=os.urandom(24))
app.include_router(auth.router)

# Include routers
app.include_router(auth.router)
app.include_router(agent.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
