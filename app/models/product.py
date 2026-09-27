from sqlalchemy import String,Column,Integer,Boolean,Text,Numeric,Float,DateTime
from sqlalchemy.orm import Mapped,mapped_column
from datetime import datetime,timezone


from app.database import Base


class Product(Base):

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )


    name: Mapped[str] = mapped_column(
        String(200)
    )
    category:Mapped[str]=mapped_column(String(100))
    description: Mapped[str] = mapped_column(
        Text
    )

    price: Mapped[float] = mapped_column(
        Numeric(10, 2)
    )

    stock: Mapped[int] = mapped_column(
        Integer
    )
    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc)
)

    offer:Mapped[int]=mapped_column(Integer,default=0)

    image: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )
