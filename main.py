from fastapi import FastAPI
from routers import market, user
from core.database import engine , SessionLocal
from core import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(market.market)
app.include_router(market.mType)

@app.get("/")
async def root():
    return {"message": "Hello World"}