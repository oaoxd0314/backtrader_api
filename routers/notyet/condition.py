from fastapi import APIRouter,Depends,HTTPException
from typing import List
from core.dependencies import get_db
from sqlalchemy.orm import Session
from core import crud,schemas

router = APIRouter(
    prefix="/condition",
    tags=["condition"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model= List[schemas.Condition])
def get_all_conditions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_condition(db, skip=skip, limit=limit)

@router.get("/{condition_id}",response_model= schemas.Condition)
def get_condition(condition_id: int = 0, db: Session = Depends(get_db)):
    condition = crud.get_condition_by_id(db, id=condition_id)
    if (condition):
        return condition
    raise HTTPException(status_code=400, detail=f"condition id {condition_id} not found, plz check again")

@router.post("/",response_model=schemas.Condition)
def create_condition(condition: schemas.ConditionBase, db: Session = Depends(get_db)):
    db_condition = crud.get_condition_by_email(db,email=condition.email)
    if db_condition:
        raise HTTPException(status_code=400, detail=f"email {condition.email} has been register")
    return crud.create_condition(db,condition)

@router.delete("/",response_model=schemas.Condition)
def delete_condition(condition: schemas.Condition, db: Session = Depends(get_db)):
    db_condition = crud.get_condition_by_id(db, id=condition.id)
    if(db_condition):
        return crud.delete_condition(db,condition)

    raise HTTPException(status_code=400, detail=f"condition id {condition.id} not found, plz check again")

@router.put("/",response_model=schemas.Condition) 
def update_condition(condition: schemas.Condition, db: Session = Depends(get_db)):
    db_condition = crud.get_condition_by_id(db, id= condition.id)
    if(db_condition):
        return crud.update_condition(db,condition)

    raise HTTPException(status_code=400, detail=f"condition id {condition.id} not found, plz check again")

