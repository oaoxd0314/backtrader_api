from fastapi import APIRouter,Depends,HTTPException
from typing import List
from core.dependencies import get_db
from sqlalchemy.orm import Session
from core import crud,schemas

router = APIRouter(
    prefix="/product",
    tags=["product"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model= List[schemas.Product])
def get_all_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_product(db, skip=skip, limit=limit)

@router.get("/{product_id}",response_model= schemas.Product)
def get_product(product_id: int = 0, db: Session = Depends(get_db)):
    product = crud.get_product_by_id(db, id=product_id)
    if (product):
        return product
    raise HTTPException(status_code=400, detail=f"product id {product_id} not found, plz check again")

@router.post("/",response_model=schemas.Product)
def create_product(product: schemas.ProductBase, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_email(db,email=product.email)
    if db_product:
        raise HTTPException(status_code=400, detail=f"email {product.email} has been register")
    return crud.create_product(db,product)

@router.delete("/",response_model=schemas.Product)
def delete_product(product: schemas.Product, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_id(db, id=product.id)
    if(db_product):
        return crud.delete_product(db,product)

    raise HTTPException(status_code=400, detail=f"product id {product.id} not found, plz check again")

@router.put("/",response_model=schemas.Product) 
def update_product(product: schemas.Product, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_id(db, id= product.id)
    if(db_product):
        return crud.update_product(db,product)

    raise HTTPException(status_code=400, detail=f"product id {product.id} not found, plz check again")

