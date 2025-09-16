from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://postgres:newnew@localhost:5432/fastapi"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)