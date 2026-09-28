from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import SESSION_SECRET
from app.routers.admin import router as admin_router
from app.database import Base,engine
from app.routers.home import router as home_router

app=FastAPI(title="Saree app")

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET
)

router_list=[home_router,admin_router]
for router in router_list:
    app.include_router(router)

Base.metadata.create_all(bind=engine)

app.mount(
    "/files",
    StaticFiles(directory="uploads"),
    name="files"
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

