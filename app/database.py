from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase

url="sqlite:///test.db"

engine=create_engine(url)
SessionLocal=sessionmaker(
    bind=engine,autoflush=False,autocommit=False
)

class Base(DeclarativeBase):
    pass

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
