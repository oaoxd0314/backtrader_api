from fastapi import APIRouter,Depends,HTTPException
from typing import List
from core.dependencies import get_db
from sqlalchemy.orm import Session
from core import crud,schemas

router = APIRouter(
    prefix="/productType",
    tags=["productType"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model= List[schemas.ProductType])
def get_all_productTypes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_productType(db, skip=skip, limit=limit)

@router.get("/{productType_id}",response_model= schemas.ProductType)
def get_productType(productType_id: int = 0, db: Session = Depends(get_db)):
    productType = crud.get_productType_by_id(db, id=productType_id)
    if (productType):
        return productType
    raise HTTPException(status_code=400, detail=f"productType id {productType_id} not found, plz check again")

@router.post("/",response_model=schemas.ProductType)
def create_productType(productType: schemas.ProductTypeBase, db: Session = Depends(get_db)):
    db_productType = crud.get_productType_by_email(db,email=productType.email)
    if db_productType:
        raise HTTPException(status_code=400, detail=f"email {productType.email} has been register")
    return crud.create_productType(db,productType)

@router.delete("/",response_model=schemas.ProductType)
def delete_productType(productType: schemas.ProductType, db: Session = Depends(get_db)):
    db_productType = crud.get_productType_by_id(db, id=productType.id)
    if(db_productType):
        return crud.delete_productType(db,productType)

    raise HTTPException(status_code=400, detail=f"productType id {productType.id} not found, plz check again")

@router.put("/",response_model=schemas.ProductType) 
def update_productType(productType: schemas.ProductType, db: Session = Depends(get_db)):
    db_productType = crud.get_productType_by_id(db, id= productType.id)
    if(db_productType):
        return crud.update_productType(db,productType)

    raise HTTPException(status_code=400, detail=f"productType id {productType.id} not found, plz check again")

