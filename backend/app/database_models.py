from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, Column, String, Float

Base = declarative_base()

class Product(Base):
    
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name= Column(String(50), nullable=False)
    description= Column(String)
    price= Column(Float)
    quantity= Column(Integer)