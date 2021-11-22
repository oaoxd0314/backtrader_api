from sqlalchemy.orm import Session, query, session
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql.functions import mode
from core.database import cursor,connection
from distutils.util import strtobool
from core import models,schemas,helper

# user
def get_all_user(db: Session, skip: int = 0, limit: int = 100):
    # return db.query(models.User).offset(skip).limit(limit).all()
    users = []
    query_users = "SELECT * FROM user LIMIT ? OFFSET ?"
    for item in cursor.execute(query_users,(limit,skip)):
        user = helper.build_model(cursor.description,item,models.User)
        user.strategy_list = get_all_strategy_by_id(db=db,id=item[0])
        
        users.append(user)
    return users

def get_user_by_id(db: Session, id: int):
    query_user = "SELECT * FROM user WHERE id = ?"
    db_user = cursor.execute(query_user,[id]).fetchone()
    if(db_user):
        user = helper.build_model(cursor.description,db_user,models.User)
        user.strategy_list = get_all_strategy_by_id(db=db,id=db_user[0])
        return user

def get_user_by_email(db: Session, email: str):
    # return db.query(models.User).filter(models.User.email == email).first()
    query_user = "SELECT * FROM user WHERE email = ?"
    db_user = cursor.execute(query_user,[email]).fetchone()
    if(db_user):
        return db_user
    
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    query = "INSERT INTO user (name,email,hashed_password) VALUES (?,?,?)"
    cursor.execute(query,[user.name,user.email,fake_hashed_password])
    connection.commit()
    
    db_user = get_user_by_email(db,user.email)
    return helper.build_model(cursor.description,db_user,models.User)

def delete_user(db: Session,user:schemas.User):
    query = "DELETE FROM user WHERE id = ? AND email = ? AND name = ?"
    cursor.execute(query,[user.id,user.email,user.name])
    connection.commit()

    return user

def update_user(db: Session,user:schemas.User):
    query = "UPDATE user SET name = ?, is_active = ? WHERE id = ? AND email = ?"

    cursor.execute(query,[user.name,user.is_active,user.id,user.email])
    connection.commit()

    return get_user_by_id(db,id=user.id)

#strategy
def admin_get_all_strategy(db:Session, skip: int = 0, limit: int = 100):
    query_all = "SELECT * FROM strategy LIMIT ? OFFSET ?"
    strategys= []
    for item in cursor.execute(query_all,[limit,skip]):
        dict = helper.create_model_dict(cursor.description,item)
        strategy = models.Strategy(**dict)
        strategys.append(strategy)
    return strategys

def get_all_strategy_by_id(db:session,id: int, skip: int = 0, limit: int = 100):
    # 會被重複 call 的子 model 就需要在 function 內自行生成 cursor
    # 因為 sqlite 不支援並行
    cur = connection.cursor()
    query_all = "SELECT strategy.* FROM strategy,user WHERE user.id = strategy.owner_id AND strategy.owner_id = ? LIMIT ? OFFSET ?"
    strategys= []
    for item in cur.execute(query_all,[id,limit,skip]):
        strategy = helper.build_model(cur.description,item,models.Strategy)
        strategys.append(strategy)

    return strategys

def get_strategy_by_id(db:Session, o_id: int, s_id: int):
    query = "SELECT * FROM strategy WHERE owner_id =? AND id = ?"
    db_strategy = cursor.execute(query,[o_id,s_id]).fetchone()
    if(db_strategy):
        return helper.build_model(cursor.description,db_strategy,models.Strategy)

def get_strategy_by_name(db:Session, o_id: int, name:str):
    query = "SELECT * FROM strategy WHERE owner_id =? AND name = ?"
    db_strategy = cursor.execute(query,[o_id,name]).fetchone()
    if(db_strategy):
        return helper.build_model(cursor.description,db_strategy,models.Strategy)

def create_strategy(db:Session, strategy:schemas.StrategyBase):
    query = "INSERT INTO strategy (name,description,initfunds,unit,sdate,edate,owner_id) VALUES (?,?,?,?,?,?,?)"
    param = list(strategy.dict().values())
    cursor.execute(query,[*param])
    connection.commit()

    db_strategy = get_strategy_by_name(db= db,o_id= param[6],name = strategy.name)
    return db_strategy

def update_strategy(db:Session, strategy:schemas.Strategy):
    query = "UPDATE strategy SET name = ?, description = ?, initfunds = ?, unit = ?, sdate = ?, edate =?, WHERE id = ? AND owner_id =?"
    print(strategy)
    cursor.execute(query,[])
    connection.commit()
    return get_strategy_by_id(db, o_id= strategy.owner_id, s_id = strategy.id)

def delete_strategy(db:Session, strategy:schemas.Strategy):
    query = "DELETE FROM strategy WHERE id = ? AND name = ?"
    cursor.execute(query,[])
    connection.commit()
    return get_strategy_by_id(db, o_id= strategy.owner_id, s_id = strategy.id)

#asset
def get_all_asset(db:Session, skip: int = 0, limit: int = 100):
    query_all = "SELECT * FROM asset LIMIT ? OFFSET ?"
    asset= []
    for item in cursor.execute(query_all,[limit,skip]):
        asset = models.Asset(id=item[0],)
        asset.append(asset)
    return asset

def get_asset_by_id(db:Session, id:int):
    query = "SELECT * FROM asset WHERE id = ?"
    db_asset = cursor.execute(query,[id]).fetchone()
    if(db_asset):
        return models.Asset()

def get_asset_by_name(db:Session, name:str):
    query = "SELECT * FROM asset WHERE name = ?"
    db_asset = cursor.execute(query,[name]).fetchone()
    if(db_asset):
        return models.Asset()

def create_asset(db:Session, asset:schemas.Asset):
    query = "INSERT INTO asset (name) VALUES (?)"
    cursor.execute(query,[])
    connection.commit()
    return

def update_asset(db:Session, asset:schemas.Asset):
    query = "UPDATE asset SET name = ? WHERE id = ?"
    cursor.execute(query,[])
    connection.commit()
    return

def delete_asset(db:Session, asset:schemas.Asset):
    query = "DELETE FROM asset WHERE id = ? AND name = ?"
    cursor.execute(query,[])
    connection.commit()
    return

#trade
def get_all_trade(db:Session, skip: int = 0, limit: int = 100):
    query_all = "SELECT * FROM trade LIMIT ? OFFSET ?"
    trades= []
    for item in cursor.execute(query_all,[limit,skip]):
        trade = models.Trade(id=item[0],)
        trades.append(trade)
    return trades

def get_trade_by_id(db:Session, id:int):
    query = "SELECT * FROM trade WHERE id = ?"
    db_trade = cursor.execute(query,[id]).fetchone()
    if(db_trade):
        return models.Trade()

def get_trade_by_name(db:Session, name:str):
    query = "SELECT * FROM trade WHERE name = ?"
    db_trade = cursor.execute(query,[name]).fetchone()
    if(db_trade):
        return models.Trade()

def create_trade(db:Session, trade:schemas.Trade):
    query = "INSERT INTO trade (name) VALUES (?)"
    cursor.execute(query,[])
    connection.commit()
    return

def update_trade(db:Session, trade:schemas.Trade):
    query = "UPDATE trade SET name = ? WHERE id = ?"
    cursor.execute(query,[])
    connection.commit()
    return

def delete_trade(db:Session, trade:schemas.Trade):
    query = "DELETE FROM trade WHERE id = ? AND name = ?"
    cursor.execute(query,[])
    connection.commit()
    return

#condition
def get_all_condition(db:Session, skip: int = 0, limit: int = 100):
    query_all = "SELECT * FROM condition LIMIT ? OFFSET ?"
    conditions= []
    for item in cursor.execute(query_all,[limit,skip]):
        condition = models.Condition(id=item[0],)
        conditions.append(condition)
    return conditions

def get_condition_by_id(db:Session, id:int):
    query = "SELECT * FROM condition WHERE id = ?"
    db_condition = cursor.execute(query,[id]).fetchone()
    if(db_condition):
        return models.Condition()

def get_condition_by_name(db:Session, name:str):
    query = "SELECT * FROM condition WHERE name = ?"
    db_condition = cursor.execute(query,[name]).fetchone()
    if(db_condition):
        return models.Condition()

def create_condition(db:Session, condition:schemas.Condition):
    query = "INSERT INTO condition (name) VALUES (?)"
    cursor.execute(query,[])
    connection.commit()
    return

def update_condition(db:Session, condition:schemas.Condition):
    query = "UPDATE condition SET name = ? WHERE id = ?"
    cursor.execute(query,[])
    connection.commit()
    return

def delete_condition(db:Session, condition:schemas.Condition):
    query = "DELETE FROM condition WHERE id = ? AND name = ?"
    cursor.execute(query,[])
    connection.commit()
    return

# market
def get_all_market(db:Session, skip: int = 0, limit: int = 100):
    # query_all = "SELECT * FROM market LIMIT {} OFFSET {}"
    query_all = "SELECT * FROM market LIMIT ? OFFSET ?"
    users = []
    for item in cursor.execute(query_all,(limit,skip)):
        user = models.Market(id=item[0],name=item[1],type=item[2])
        users.append(user)
    return users

def get_market_by_id(db: Session, id: int):
    query = "SELECT * FROM market WHERE id = ?"
    db_market = cursor.execute(query,[id]).fetchone()

    if(db_market):
        return models.Market(id=db_market[0],name=db_market[1],type=db_market[2])

def get_market_by_name(db: Session, name: int):
    query = "SELECT * FROM market WHERE name = ?"
    db_market = cursor.execute(query,[name]).fetchone()

    if(db_market):
        return models.Market(id=db_market[0],name=db_market[1],type=db_market[2])
    

def create_market(db: Session, market: schemas.MarketCreate):
    query = "INSERT INTO market (name, type) VALUES (?,?)"
    cursor.execute(query,[market.name,market.type])
    connection.commit()

    db_market = get_market_by_name(db,market.name)
    return models.Market(id=db_market.id, name=db_market.name, type=db_market.type)

def delete_market(db: Session,market:schemas.Market):
    query = "DELETE FROM market WHERE id = ? AND name = ?"
    cursor.execute(query,[market.id,market.name])
    connection.commit()

    return market

def update_market(db: Session,market:schemas.Market):
    query = "UPDATE market SET name = ? WHERE id = ?"
    cursor.execute(query,[market.name,market.id])
    connection.commit()
    
    return get_market_by_id(db,id=market.id)

#product
def get_all_product(db:Session, skip: int = 0, limit: int = 100):
    query_all = "SELECT * FROM product LIMIT ? OFFSET ?"
    products= []
    for item in cursor.execute(query_all,[limit,skip]):
        product = models.Product(id=item[0],)
        products.append(product)
    return products

def get_product_by_id(db:Session, id:int):
    query = "SELECT * FROM product WHERE id = ?"
    db_product = cursor.execute(query,[id]).fetchone()
    if(db_product):
        return models.Product()

def get_product_by_name(db:Session, name:str):
    query = "SELECT * FROM product WHERE name = ?"
    db_product = cursor.execute(query,[name]).fetchone()
    if(db_product):
        return models.Product()

def create_product(db:Session, product:schemas.Product):
    query = "INSERT INTO product (name) VALUES (?)"
    cursor.execute(query,[])
    connection.commit()
    return

def update_product(db:Session, product:schemas.Product):
    query = "UPDATE product SET name = ? WHERE id = ?"
    cursor.execute(query,[])
    connection.commit()
    return

def delete_product(db:Session, product:schemas.Product):
    query = "DELETE FROM product WHERE id = ? AND name = ?"
    cursor.execute(query,[])
    connection.commit()
    return

#detailData
def get_all_detailData(db:Session, skip: int = 0, limit: int = 100):
    query_all = "SELECT * FROM detailData LIMIT ? OFFSET ?"
    detailDatas= []
    for item in cursor.execute(query_all,[limit,skip]):
        detailData = models.DetailData(id=item[0],)
        detailDatas.append(detailData)
    return detailDatas

def get_detailData_by_id(db:Session, id:int):
    query = "SELECT * FROM detailData WHERE id = ?"
    db_detailData = cursor.execute(query,[id]).fetchone()
    if(db_detailData):
        return models.DetailData()

def get_detailData_by_name(db:Session, name:str):
    query = "SELECT * FROM detailData WHERE name = ?"
    db_detailData = cursor.execute(query,[name]).fetchone()
    if(db_detailData):
        return models.DetailData()

def create_detailData(db:Session, detailData:schemas.DetailData):
    query = "INSERT INTO detailData (name) VALUES (?)"
    cursor.execute(query,[])
    connection.commit()
    return

def update_detailData(db:Session, detailData:schemas.DetailData):
    query = "UPDATE detailData SET name = ? WHERE id = ?"
    cursor.execute(query,[])
    connection.commit()
    return

def delete_detailData(db:Session, detailData:schemas.DetailData):
    query = "DELETE FROM detailData WHERE id = ? AND name = ?"
    cursor.execute(query,[])
    connection.commit()
    return

# mType
def get_all_mType(db: Session,skip: int = 0, limit: int = 100 ):
    query_all = "SELECT * FROM marketType LIMIT ? OFFSET ?"
    types = []
    for item in cursor.execute(query_all,(limit,skip)):
        type = models.MarketType(id=item[0],name=item[1])
        types.append(type)
    return types

def get_mType_by_id(db: Session,id: int):
    query = "SELECT * FROM marketType WHERE id = ?"
    mType = cursor.execute(query,[id]).fetchone()
    if (mType):
        return models.MarketType(id=mType[0],name=mType[1])

def get_mType_by_name(db: Session, name: str):
    query = "SELECT * FROM marketType WHERE name = ?"
    mType = cursor.execute(query,[name]).fetchone()

    if(mType):
        return models.MarketType(id=mType[0],name=mType[1])

def create_mType(db: Session, type: schemas.MarketTypeBase):
    query = "INSERT INTO marketType (name) VALUES (?)"
    cursor.execute(query,[type.name]).fetchone()
    connection.commit()

    db_mType = get_mType_by_name(db,type.name)
    return models.MarketType(id=db_mType.id,name=db_mType.name)

def update_mType(db: Session,type:schemas.MarketType):
    query = "UPDATE marketType SET name = ? WHERE id = ?"
    cursor.execute(query,[type.name,type.id])
    connection.commit()

    db_mType = get_mType_by_name(db,type.name)
    return models.MarketType(id=db_mType.id,name=db_mType.name)

def delete_mType(db: Session,type:schemas.MarketType):
    query = "DELETE FROM marketType WHERE id = ? AND name = ?"
    cursor.execute(query,[type.id,type.name])
    connection.commit()

    return type

#productType
def get_all_productType(db:Session, skip: int = 0, limit: int = 100):
    query_all = "SELECT * FROM productType LIMIT ? OFFSET ?"
    productTypes= []
    for item in cursor.execute(query_all,[limit,skip]):
        productType = models.ProductType(id=item[0],)
        productTypes.append(productType)
    return productTypes

def get_productType_by_id(db:Session, id:int):
    query = "SELECT * FROM productType WHERE id = ?"
    db_productType = cursor.execute(query,[id]).fetchone()
    if(db_productType):
        return models.ProductType()

def get_productType_by_name(db:Session, name:str):
    query = "SELECT * FROM productType WHERE name = ?"
    db_productType = cursor.execute(query,[name]).fetchone()
    if(db_productType):
        return db_productType

def create_productType(db:Session, productType:schemas.ProductType):
    query = "INSERT INTO productType (name) VALUES (?)"
    cursor.execute(query,[])
    connection.commit()
    return

def update_productType(db:Session, productType:schemas.ProductType):
    query = "UPDATE productType SET name = ? WHERE id = ?"
    cursor.execute(query,[])
    connection.commit()
    return

def delete_productType(db:Session, productType:schemas.ProductType):
    query = "DELETE FROM productType WHERE id = ? AND name = ?"
    cursor.execute(query,[])
    connection.commit()
    return