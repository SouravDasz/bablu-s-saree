from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from dotenv import load_dotenv
import os



load_dotenv()

url=os.getenv("DATABASE_URI")

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
