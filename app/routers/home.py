from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.product import Product

templates = Jinja2Templates(
    directory="app/templates"
)


router=APIRouter(tags=["HomePage"])

SAREE_CATEGORIES = [
    "Banarasi",
    "Silk",
    "Kanjivaram",
    "Tussar",
    "Muga",
    "Patola",
    "Chanderi",
    "Kota",
    "Dhakai Jamdani",
    "Jamdani",
    "Cotton Saree",
    "Tant",
    "Baluchari",
    "Others",
]


#Landing page
@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(request,"home.html")

#Home page

@router.get("/products")
def products(
    request: Request,
    search: str | None = None,
    category: str | None = None,
    price_sort: str | None = None,
    sort: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Product)

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    if category:
        query = query.filter(Product.category == category)

    if price_sort == "low_to_high":
        query = query.order_by(Product.price.asc())
    elif price_sort == "high_to_low":
        query = query.order_by(Product.price.desc())

    if sort == "oldest":
        query = query.order_by(Product.created_at.asc())
    elif sort == "newest" or not price_sort:
        query = query.order_by(Product.created_at.desc())

    products = query.all()
    categories = [row[0] for row in db.query(Product.category).distinct().order_by(Product.category).all()]

    return templates.TemplateResponse(
        request,
        "products.html",
        {
            "products": products,
            "categories": categories,
            "search": search or "",
            "category": category or "",
            "price_sort": price_sort or "",
            "sort": sort or "",
        }
    )


@router.get("/categories")
def categories(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).order_by(Product.created_at.desc()).all()
    products_by_category = {category: [] for category in SAREE_CATEGORIES}

    for product in products:
        products_by_category.setdefault(product.category, []).append(product)

    category_cards = [
        {"name": category, "products": products_by_category[category]}
        for category in SAREE_CATEGORIES
    ]

    return templates.TemplateResponse(
        request,
        "categories.html",
        {"category_cards": category_cards},
    )

@router.get("/product/{id}")
def product(request:Request,id:int,db:Session=Depends(get_db)):
    saree_details=db.query(Product).filter(Product.id==id).first()
    return templates.TemplateResponse(request,"product.html",context={
        "product":saree_details
    })
