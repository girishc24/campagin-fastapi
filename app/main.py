from datetime import datetime
from random import randint
from typing import  Any
from fastapi import FastAPI, HTTPException, Response, Depends
from models import Product
from database import session, engine
import database_models 
from sqlalchemy.orm import Session

app = FastAPI(root_path="/api/v1")

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello World!"}

# Campaigns
# - campaign_id: int
# - name: str
# - due_date: date
# - created_at: date

data = [
    {
        "campaign_id": 1,
        "name": "Campaign 1",
        "due_date": datetime.now(),
        "created_at": datetime.now()
    },
    {
        "campaign_id": 2,
        "name": "Campaign 2",
        "due_date": datetime.now(),
        "created_at": datetime.now()
    }
]

products = [
    Product(id=1, name="phone", description="Hello", price=10, quantity=1),
    Product(id=2, name="phone", description="Hello", price=10, quantity=1),
    Product(id=3, name="phone", description="Hello", price=10, quantity=1),
    Product(id=4, name="phone", description="Hello", price=10, quantity=1),
    Product(id=5, name="phone", description="Hello", price=10, quantity=1),
    Product(id=6, name="phone", description="Hello", price=10, quantity=1)
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
 
def init_db():
    db = session()
    count = db.query(database_models.Product).count 
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))

        db.commit()
init_db()

@app.get("/campaigns")
async def get_campaigns():
    return {"campaigns": data}

@app.get("/campaigns/{campaign_id}")
async def get_campaigns(campaign_id: int):
    for campagin in data:
        if campagin.get("campaign_id") == campaign_id:
            return {"campaign": campagin}
    raise HTTPException(status_code=404, detail="Campaign not found")

@app.post("/campaigns")
async def get_campaigns(body: dict[str, Any]):

    new_campaign = {
        "campaign_id": randint(3, 1000),
        "name": body.get("name"),
        "due_date": body.get("due_date"),
        "created_at": datetime.now()
    }
    data.append(new_campaign)
    return {"campaign": new_campaign}

@app.put("/campaigns/{campaign_id}")
async def update_campaign(campaign_id: int, body: dict[str,Any]):
    for index, campaign in enumerate(data):
        if campaign.get("campaign_id") == campaign_id:
            update = {
                "campaign_id": campaign_id,
                "name": body.get("name"),
                "due_date": body.get("due_date"),
                "created_at": campaign.get("created_at")
            }
            data[index] = update
            return {"campaign": update}
    raise HTTPException(status_code=404, detail="Campaign not found")

@app.delete("/campaigns/{campaign_id}")
async def update_campaign(campaign_id: int):
    for index, campaign in enumerate(data):
        if campaign.get("campaign_id") == campaign_id:
            data.pop(index)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Campaign not found")

@app.get("/items")
async def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/products")
async def get_products(db: Session = Depends(get_db)): # Dependency Injection of database
    #db = session()
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/products/{product_id}")
async def get_products_id(product_id : int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    # for product in products:
    #     if product.id == product_id:
    #         return product
    if db_product:
        return db_product
    raise HTTPException(status_code=404, detail="No Products Found")

@app.post("/produts")
async def add_product(product: Product, db: Session = Depends(get_db)):
    #products.append(product)
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products")
async def update_product(product_id : int, product : Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return {"message": "Product Updated"}
    # for i in range(len(products)):
    #     if products[i].id == product_id:
    #         products[i] = product
    #     return product
    else:
        raise HTTPException(status_code=404, detail="No Product ID")

@app.delete("/products/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return {"message": "Product Deleted Successfully"}
    # for index, product in enumerate(products):
    #     if product.get("id") == product_id:
    #         products.pop(index)
    #         return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Product not found")