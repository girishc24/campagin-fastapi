from contextlib import asynccontextmanager
from datetime import datetime
from random import randint
from typing import Annotated, Any
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlmodel import SQLModel, Session, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    # Any cleanup code can go here

app = FastAPI(root_path="/api/v1", lifespan=lifespan)

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