from fastapi import APIRouter,Form,Request,Depends,UploadFile,File
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import os
import uuid
import shutil
from sqlalchemy.orm import Session


from app.core.config import ADMIN_EMAIL,ADMIN_PASSWORD 
from app.core.auth import require_admin
from app.models.product import Product
from app.database import get_db


router=APIRouter(
    prefix="/admin",
    tags=["Admin"])

templates = Jinja2Templates(
    directory="app/templates"
)


#render login page
@router.get("/login")
def admin_login(request:Request):
    return templates.TemplateResponse(
        request=request,name="login.html"
    )

#send login request 
@router.post("/login")
def admin_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    print(email,ADMIN_EMAIL)
    print(password,ADMIN_PASSWORD)
    if email != ADMIN_EMAIL:
        return {"error": "Invalid credentials"}

    if password != ADMIN_PASSWORD:
        return {"error": "Invalid credentials"}

    request.session["admin"] = True

    return RedirectResponse(
        "/admin/dashboard",
        status_code=303
    )

#render dashbord
@router.get("/dashboard")
def dashboard(request:Request,admin=Depends(require_admin)):

    return templates.TemplateResponse(request=request,name="admin/dashboard.html")


#Adding new product

@router.get("/products/add")
def add_products(request:Request):
    return templates.TemplateResponse(request,name="admin/product_add.html")

@router.post("/products/add")
def add_product(
    request: Request,

    name: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),

    image: UploadFile = File(...),

    db: Session = Depends(get_db),

    admin=Depends(require_admin)
):

    upload_dir = "uploads/products"

    os.makedirs(upload_dir, exist_ok=True)

    extension = os.path.splitext(image.filename)[1]

    filename = f"{uuid.uuid4()}{extension}"

    file_path = os.path.join(
        upload_dir,
        filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            image.file,
            buffer
        )

    product = Product(
        name=name,
        category=category,
        description=description,
        price=price,
        stock=stock,
        image=filename
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return RedirectResponse(
        "/admin/products",
        status_code=303
    )

#Show existing products

@router.get("/products")
def products(
    request: Request,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    products = db.query(Product).all()

    return templates.TemplateResponse(
        request,
        "admin/products.html",
        {
        
            "products": products
        }
    )

@router.get("/products/edit/{id}")
def edit_product(
    request:Request,
    id:int,
    db:Session=Depends(get_db),
    admin=Depends(require_admin)):

    product=db.query(Product).filter(Product.id==id).first()

    if not product:
        return RedirectResponse(
            url="/admin/products",
            status_code=303
        )
    return templates.TemplateResponse(
        request,"admin/edit_product.html",context={
            "product":product
        }
    )

@router.post("/products/edit/{id}")
def update_product(
    request: Request,
    id: int,
    name: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    # 1. Find the product
    product = db.query(Product).filter(Product.id == id).first()

    # 2. If product doesn't exist
    if not product:
        return RedirectResponse(
            "/admin/products",
            status_code=303
        )

    # 3. Update normal fields
    product.name = name
    product.category = category
    product.description = description
    product.price = price
    product.stock = stock

    # 4. Handle new image
    if image and image.filename:

        upload_dir = "uploads/products"
        os.makedirs(upload_dir, exist_ok=True)

        extension = os.path.splitext(image.filename)[1]

        filename = f"{uuid.uuid4()}{extension}"

        file_path = os.path.join(
            upload_dir,
            filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                image.file,
                buffer
            )

        product.image = filename

    # 5. Save changes
    db.commit()

    # 6. Go back to products page
    return RedirectResponse(
        "/admin/products",
        status_code=303
    )


#Delete product

@router.post("/products/delete/{id}")
def delete_product(
    id:int,
    db:Session=Depends(get_db),
    admin=Depends(require_admin)):
    product=db.query(Product).filter(Product.id==id).first()
    
    if not product:
        return RedirectResponse(
            "/admin/products",
            status_code=303
        )
    db.delete(product)
    db.commit()
    return RedirectResponse(
            "/admin/products",
            status_code=303
            )
