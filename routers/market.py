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


@market.get("/{market_id}", response_model=schemas.Market)
def get_market(market_id: int = 0,db: Session = Depends(get_db)):
    market = crud.get_market_by_id(db, id= market_id) 
    if(market):
        return market
    raise HTTPException(status_code=400, detail=f"market id {market_id} not found, plz check again")
    

@market.post("/", response_model = schemas.Market)
def create_market(market: schemas.MarketCreate, db: Session = Depends(get_db)):
    db_market = crud.get_market_by_name(db,name = market.name)
    if(db_market):
        raise HTTPException(status_code=400, detail=f"market '{market.name}' already exist")
    
    return crud.create_market(db,market)


@market.delete("/", response_model = schemas.Market)
def delete_market(market: schemas.Market, db: Session = Depends(get_db)):
    db_market = crud.get_market_by_id(db, id= market.id)
    if(db_market):
        return crud.delete_market(db,market)

    raise HTTPException(status_code=400, detail=f"market id {market.id} not found, plz check again")
    

@market.put("/",response_model = schemas.Market)
def update_market(market: schemas.Market, db: Session = Depends(get_db)):
    db_market = crud.get_market_by_id(db, id= market.id)
    if(db_market):
        return crud.update_market(db,market)

    raise HTTPException(status_code=400, detail=f"market id {market.id} not found, plz check again")


# market-type
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
    db_mType = crud.get_mType_by_name(db,type.name)

    if (db_mType):
        raise HTTPException(status_code=400, detail=f"market type '{type.name}' alerady exist")
    return crud.create_mType(db,type)

@mType.delete("/")
def delete_market_type(type: schemas.MarketType, db: Session = Depends(get_db)):
    mType = crud.get_mType_by_id(db, id=type.id)
    if(mType):
        return crud.delete_mType(db,type)

    raise HTTPException(status_code=400, detail=f"market id {type.id} not found, plz check again")

@mType.put("/",response_model = schemas.MarketType)
def update_market_type(type: schemas.MarketType, db: Session = Depends(get_db)):
    mType = crud.get_mType_by_id(db, id=type.id)
    if(mType):
        return crud.update_mType(db,type)

    raise HTTPException(status_code=400, detail=f"mType id {type.id} not found, plz check again")