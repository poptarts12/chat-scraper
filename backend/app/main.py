# backend/app/main.py

from fastapi import FastAPI
from app.database import engine
from app.models.user import Base as UserBase
from app.models.conversation import Base as ConvBase
from app.models.message import Base as MsgBase
from app.database import Base, engine
Base.metadata.create_all(bind=engine)

from app.api.auth import router as auth_router
from app.api.conversations import router as conv_router
from app.api.messages import router as msg_router

# create all tables
UserBase.metadata.create_all(bind=engine)
ConvBase.metadata.create_all(bind=engine)
MsgBase.metadata.create_all(bind=engine)

app = FastAPI(
    title="ChatGPT Saver API",
    version="1.0.0",
    docs_url="/docs"
)

app.include_router(auth_router)
app.include_router(conv_router)
app.include_router(msg_router)
