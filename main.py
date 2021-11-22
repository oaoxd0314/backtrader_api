from fastapi import FastAPI
from routers.notyet import asset,condition,detailData,product,productType,trade
from routers import market, user, strategy
from core.database import engine , SessionLocal
from core import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(market.market)
app.include_router(market.mType)
app.include_router(strategy.router)
app.include_router(asset.router)
app.include_router(condition.router)
app.include_router(detailData.router)
app.include_router(product.router)
app.include_router(productType.router)
app.include_router(trade.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}