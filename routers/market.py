from core.models import Market
from fastapi import APIRouter,Depends,HTTPException
from typing import List
from core.dependencies import get_db
from sqlalchemy.orm import Session
from core import crud,schemas


market = APIRouter(
    prefix="/market",
    tags=["market"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@market.get("/", response_model=List[schemas.Market])
def get_all_markets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)): 
    return crud.get_all_market(db, skip=skip, limit=limit)


@market.post("/", response_model = schemas.Market)
def create_market(market: schemas.MarketCreate, db: Session = Depends(get_db)):
    db_market = crud.get_market_by_name(db,name = market.name)
    print(db_market)
    if(db_market):
        raise HTTPException(status_code=400, detail=f"market {market.name} already exist")
    return crud.create_market(db,market)


mType = APIRouter(
    prefix="/market-type",
    tags=["market-type"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@mType.get('/',response_model = List[schemas.MarketType])
def get_all_market_type(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_mType(db, skip=skip, limit=limit)

@mType.post('/',response_model = schemas.MarketType)
def create_market_type(type: schemas.MarketTypeBase, db: Session = Depends(get_db)):
    mType = crud.get_type_by_name(db,type.name)
    if mType:
        raise HTTPException(status_code=400, detail=f"market type {mType.name} alerady exist")
    return crud.create_mType(db,type)