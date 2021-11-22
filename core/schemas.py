from typing import List, Optional

from datetime import datetime
from pydantic import BaseModel

# user
class AssetBase(BaseModel):
    name: str
    buy_time: datetime
    unit_price:int
    quantity:int
    unit: str

class Asset(AssetBase):
    id:int
    strategy_id:int
    class Config:
        orm_mode = True

class ConditionBase(BaseModel):
    status: str
    price: int
    var: Optional[str] = None

class Condition(ConditionBase):
    id: int
    trade_id: int
    class Config:
        orm_mode = True

class TradeBase(BaseModel):
    product_id: int

class Trade(TradeBase):
    condition_list: List[Condition] = []
    strategy_id: int
    id: int
    class Config:
        orm_mode = True

class StrategyBase(BaseModel):
    name : str
    description : Optional[str] = None
    initfunds: int
    unit: str
    sdate: datetime
    edate: datetime
    owner_id:int

class Strategy(StrategyBase):
    id:int
    trade_list: List[Trade] = []
    asset_list: List[Asset] = []
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name:str
    email:str
    
class UserCreate(UserBase):
    password:str

class User(UserBase):
    id: int
    is_active: bool
    strategy_list: List[Strategy] = []
    class Config:
        orm_mode = True

# market
class DetailData(BaseModel):
    id : int
    prod_id : int
    time : datetime
    open : int
    high : int
    low : int
    close : int

class ProductBase(BaseModel):
    market_id: int
    name: str
    symbol: str
    describe: Optional[str] = None

class Product(ProductBase):
    id: int
    data_list: List[DetailData] = []
    class Config:
        orm_mode = True

class MarketBase(BaseModel):
    name: str
    type: str

class MarketCreate(MarketBase):
    pass

class Market(MarketBase):
    id:int
    prod_list: List[Product] = []
    class Config:
        orm_mode = True

# type
class ProductTypeBase(BaseModel):
    name: str
    mType_id: int

class ProductType(ProductTypeBase):
    id: int
    class Config:
        orm_mode = True

class MarketTypeBase(BaseModel):
    name: str

class MarketType(MarketTypeBase):
    id: int
    prod_type: List[ProductType] = []
    class Config:
        orm_mode = True