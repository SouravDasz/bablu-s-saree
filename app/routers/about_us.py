from fastapi import APIRouter,Request
from .home import templates


router=APIRouter()


@router.get("/about")
def about(request:Request):
    return templates.TemplateResponse(request,"about.html")


@router.get("/contact")
def contact(request: Request):
    return templates.TemplateResponse(request, "contact.html")
