from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import SESSION_SECRET
from app.routers.admin import router as admin_router
from app.database import Base,engine


app=FastAPI(title="Saree app")

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET
)

app.include_router(admin_router)

Base.metadata.create_all(bind=engine)
app.mount(
    "/files",
    StaticFiles(directory="uploads"),
    name="files"
)

@app.get("/")
def home():
    return {"api testing"}