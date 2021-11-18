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
def get_all_users(user_id: int = 0, db: Session = Depends(get_db)):
    return crud.get_user_by_id(db, user_id=user_id)

@router.post("/",response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db,email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail=f"email {user.email} has been register")
    return crud.create_user(db,user)

