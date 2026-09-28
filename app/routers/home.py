from fastapi import APIRouter,Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(
    directory="app/templates"
)


router=APIRouter(tags=["HomePage"])

@router.get("/")
def home(request:Request):
    return templates.TemplateResponse(
        request,"home.html"
    )
