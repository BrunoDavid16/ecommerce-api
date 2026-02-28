from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "sqlite:///ecommerce.db"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(engine)