from fastapi import APIRouter,Depends,HTTPException
from typing import List
from core.dependencies import get_db
from sqlalchemy.orm import Session
from core import crud,schemas

router = APIRouter(
    prefix="/detailData",
    tags=["detailData"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model= List[schemas.DetailData])
def get_all_detailDatas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_detailData(db, skip=skip, limit=limit)

@router.get("/{detailData_id}",response_model= schemas.DetailData)
def get_detailData(detailData_id: int = 0, db: Session = Depends(get_db)):
    detailData = crud.get_detailData_by_id(db, id=detailData_id)
    if (detailData):
        return detailData
    raise HTTPException(status_code=400, detail=f"detailData id {detailData_id} not found, plz check again")

@router.post("/",response_model=schemas.DetailData)
def create_detailData(detailData: schemas.DetailData, db: Session = Depends(get_db)):
    db_detailData = crud.get_detailData_by_email(db,email=detailData.email)
    if db_detailData:
        raise HTTPException(status_code=400, detail=f"email {detailData.email} has been register")
    return crud.create_detailData(db,detailData)

@router.delete("/",response_model=schemas.DetailData)
def delete_detailData(detailData: schemas.DetailData, db: Session = Depends(get_db)):
    db_detailData = crud.get_detailData_by_id(db, id=detailData.id)
    if(db_detailData):
        return crud.delete_detailData(db,detailData)

    raise HTTPException(status_code=400, detail=f"detailData id {detailData.id} not found, plz check again")

@router.put("/",response_model=schemas.DetailData) 
def update_detailData(detailData: schemas.DetailData, db: Session = Depends(get_db)):
    db_detailData = crud.get_detailData_by_id(db, id= detailData.id)
    if(db_detailData):
        return crud.update_detailData(db,detailData)

    raise HTTPException(status_code=400, detail=f"detailData id {detailData.id} not found, plz check again")

