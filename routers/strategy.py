from sqlalchemy.sql.functions import user
from fastapi import APIRouter,Depends,HTTPException
from typing import List
from core.dependencies import get_db
from sqlalchemy.orm import Session
from core import crud,schemas

router = APIRouter(
    prefix="/strategy",
    tags=["strategy"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

#admin
@router.get("/admin",response_model= List[schemas.Strategy])
def admin_get_all_strategy(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.admin_get_all_strategy(db, skip=skip, limit=limit)

# strategy
@router.get("/{owner_id}",response_model= List[schemas.Strategy])
def get_all_strategy(owner_id:int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_strategy_by_id(db, id=owner_id, skip=skip, limit=limit)

@router.get("/{owner_id}/{strategy_id}",response_model= schemas.Strategy)
def get_strategy(owner_id:int, strategy_id: int = 0, db: Session = Depends(get_db)):
    strategy = crud.get_strategy_by_id(db, o_id= owner_id, s_id=strategy_id)
    if (strategy):
        return strategy
    raise HTTPException(status_code=400, detail=f"strategy id {strategy_id} not found, plz check again")

@router.post("/{owner_id}",response_model=schemas.Strategy)
def create_strategy(owner_id:int, strategy: schemas.StrategyBase, db: Session = Depends(get_db)):
    db_strategy = crud.get_strategy_by_name(db, o_id= owner_id, name=strategy.name)
    if db_strategy:
        raise HTTPException(status_code=400, detail=f"strategy {strategy.name} has been register")
    return crud.create_strategy(db,strategy)

@router.delete("/{owner_id}",response_model=schemas.Strategy)
def delete_strategy(owner_id:int, strategy: schemas.Strategy, db: Session = Depends(get_db)):
    db_strategy = crud.get_strategy_by_id(db,o_id= owner_id, s_id=strategy.id)
    if(db_strategy):
        return crud.delete_strategy(db,strategy)

    raise HTTPException(status_code=400, detail=f"user {owner_id} doesn't have strategy {strategy.id}, plz check again")

@router.put("/{owner_id}",response_model=schemas.Strategy) 
def update_strategy(owner_id:int, strategy: schemas.Strategy, db: Session = Depends(get_db)):
    db_strategy = crud.get_strategy_by_id(db,o_id= owner_id, s_id=strategy.id)
    if(db_strategy):
        return crud.update_strategy(db,strategy)

    raise HTTPException(status_code=400, detail=f"user {owner_id} doesn't have strategy {strategy.id}, plz check again")

