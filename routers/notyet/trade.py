from fastapi import APIRouter,Depends,HTTPException
from typing import List
from core.dependencies import get_db
from sqlalchemy.orm import Session
from core import crud,schemas

router = APIRouter(
    prefix="/trade",
    tags=["trade"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model= List[schemas.Trade])
def get_all_trades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_trade(db, skip=skip, limit=limit)

@router.get("/{trade_id}",response_model= schemas.Trade)
def get_trade(trade_id: int = 0, db: Session = Depends(get_db)):
    trade = crud.get_trade_by_id(db, id=trade_id)
    if (trade):
        return trade
    raise HTTPException(status_code=400, detail=f"trade id {trade_id} not found, plz check again")

@router.post("/",response_model=schemas.Trade)
def create_trade(trade: schemas.TradeBase, db: Session = Depends(get_db)):
    db_trade = crud.get_trade_by_email(db,email=trade.email)
    if db_trade:
        raise HTTPException(status_code=400, detail=f"email {trade.email} has been register")
    return crud.create_trade(db,trade)

@router.delete("/",response_model=schemas.Trade)
def delete_trade(trade: schemas.Trade, db: Session = Depends(get_db)):
    db_trade = crud.get_trade_by_id(db, id=trade.id)
    if(db_trade):
        return crud.delete_trade(db,trade)

    raise HTTPException(status_code=400, detail=f"trade id {trade.id} not found, plz check again")

@router.put("/",response_model=schemas.Trade) 
def update_trade(trade: schemas.Trade, db: Session = Depends(get_db)):
    db_trade = crud.get_trade_by_id(db, id= trade.id)
    if(db_trade):
        return crud.update_trade(db,trade)

    raise HTTPException(status_code=400, detail=f"trade id {trade.id} not found, plz check again")

