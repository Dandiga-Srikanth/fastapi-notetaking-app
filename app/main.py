from fastapi import FastAPI
from app.api import user
from app.api import auth
from app.api import note

from app.middleware.request_logger import RequestLoggerMiddleware
from app.middleware.auth_header import AuthHeaderMiddleware
from app.middleware.global_exception_handler import ExceptionHandlerMiddleware

app = FastAPI()

app.add_middleware(ExceptionHandlerMiddleware)
app.add_middleware(AuthHeaderMiddleware)
app.add_middleware(RequestLoggerMiddleware)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(note.router)