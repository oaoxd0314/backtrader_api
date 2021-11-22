from fastapi import APIRouter,Depends,HTTPException
from typing import List
from core.dependencies import get_db
from sqlalchemy.orm import Session
from core import crud,schemas

router = APIRouter(
    prefix="/asset",
    tags=["asset"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model= List[schemas.Asset])
def get_all_asset(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_asset(db, skip=skip, limit=limit)

@router.get("/{asset_id}",response_model= schemas.Asset)
def get_asset(asset_id: int = 0, db: Session = Depends(get_db)):
    asset = crud.get_asset_by_id(db, id=asset_id)
    if (asset):
        return asset
    raise HTTPException(status_code=400, detail=f"asset id {asset_id} not found, plz check again")

@router.post("/",response_model=schemas.Asset)
def create_asset(asset: schemas.AssetBase, db: Session = Depends(get_db)):
    db_asset = crud.get_asset_by_email(db,email=asset.email)
    if db_asset:
        raise HTTPException(status_code=400, detail=f"email {asset.email} has been register")
    return crud.create_asset(db,asset)

@router.delete("/",response_model=schemas.Asset)
def delete_asset(asset: schemas.Asset, db: Session = Depends(get_db)):
    db_asset = crud.get_asset_by_id(db, id=asset.id)
    if(db_asset):
        return crud.delete_asset(db,asset)

    raise HTTPException(status_code=400, detail=f"asset id {asset.id} not found, plz check again")

@router.put("/",response_model=schemas.Asset) 
def update_asset(asset: schemas.Asset, db: Session = Depends(get_db)):
    db_asset = crud.get_asset_by_id(db, id= asset.id)
    if(db_asset):
        return crud.update_asset(db,asset)

    raise HTTPException(status_code=400, detail=f"asset id {asset.id} not found, plz check again")

