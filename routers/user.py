from fastapi import APIRouter,Depends,HTTPException
from typing import List
from core.dependencies import get_db
from sqlalchemy.orm import Session
from core import crud,schemas

router = APIRouter(
    prefix="/user",
    tags=["user"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model= List[schemas.User])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_user(db, skip=skip, limit=limit)

@router.get("/{user_id}",response_model= schemas.User)
def get_user(user_id: int = 0, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, id=user_id)
    if (user):
        return user
    raise HTTPException(status_code=400, detail=f"user id {user_id} not found, plz check again")

@router.post("/",response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db,email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail=f"email {user.email} has been register")
    return crud.create_user(db,user)

@router.delete("/",response_model=schemas.User)
def delete_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, id=user.id)
    if(db_user):
        return crud.delete_user(db,user)

    raise HTTPException(status_code=400, detail=f"user id {user.id} not found, plz check again")

@router.put("/",response_model=schemas.User) 
def update_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, id= user.id)
    if(db_user):
        return crud.update_user(db,user)

    raise HTTPException(status_code=400, detail=f"user id {user.id} not found, plz check again")
