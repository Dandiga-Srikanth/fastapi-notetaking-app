from fastapi import FastAPI
from app.api import user
from app.api import auth
from app.api import note

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(note.router)