from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import foreign
from sqlalchemy.sql.sqltypes import TIMESTAMP
from datetime import datetime

from core.database import Base

# user
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    
    is_active = Column(Boolean, server_default='1')

    strategy_list = relationship("Strategy", back_populates="owner")

    # def __init__(self, id, name, email, hashed_password, is_active):
    #     self.id = id
    #     self.name = name
    #     self.email = email
    #     self.hashed_password = hashed_password
    #     is_active = bool(is_active)

class Strategy(Base):
    __tablename__ = "strategy"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    initfunds = Column(Integer)
    unit = Column(String)
    sdate = Column(TIMESTAMP)
    edate = Column(TIMESTAMP)

    owner_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates= "strategy_list")
    trade_list = relationship("Trade", back_populates= "strategy")
    asset_list = relationship("Asset", back_populates= "strategy")
class Asset(Base):
    __tablename__ = "asset"
    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategy.id"))

    buy_time = Column(TIMESTAMP)
    unit_price = Column(Integer)  
    quantity = Column(Integer)
    unit = Column(String)

    strategy = relationship("Strategy", back_populates="asset_list")


class Trade(Base):
    __tablename__ = "trade"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    strategy_id = Column(Integer, ForeignKey("strategy.id"))
    
    strategy = relationship("Strategy", back_populates="trade_list")
    condition_list = relationship("Condition", back_populates="trade")
    

class Condition(Base):
    __tablename__ = "condition"
    id = Column(Integer, primary_key=True, index=True)
    trade_id = Column(Integer, ForeignKey("trade.id"))

    status = Column(String)
    price = Column(Integer)
    var = Column(String)
    trade = relationship("Trade", back_populates="condition_list")

# market 
class Market(Base):
    __tablename__ = "market"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    type = Column(Integer, ForeignKey("marketType.name"))
    prod_list = relationship("Product", back_populates="market")

class Product(Base):
    __tablename__ = "product"
    
    id = Column(Integer, primary_key=True, index=True)
    market_id = Column(Integer, ForeignKey("market.id"))
    name = Column(String)
    describe = Column(String)
    symbol = Column(String)
    market = relationship("Market", back_populates="prod_list")
    data_list = relationship("DetailData", back_populates="product")

class DetailData(Base):
    __tablename__ = "detail_data"

    id = Column(Integer, primary_key=True, index=True)
    prod_id = Column(Integer, ForeignKey("product.id"))
    time = Column(TIMESTAMP)
    product = relationship("Product", back_populates="data_list")
    open = Column(Integer)
    high = Column(Integer)
    low = Column(Integer)
    close = Column(Integer)

class MarketType(Base):
    __tablename__ = "marketType"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    prod_type = relationship("ProductType", back_populates="mType")

class ProductType(Base):
    __tablename__ = "productType"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    mType_id = Column(Integer,ForeignKey("marketType.id"))
    mType = relationship("MarketType", back_populates="prod_type")