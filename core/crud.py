from sqlalchemy.orm import Session, query
from core.database import cursor

from core import models,schemas

# user
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(name=user.name,email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    query_user = "SELECT * FROM user WHERE id = ?"
    user = cursor.execute(query_user,[user_id]).fetchone()

    return models.User(id=user[0],email=user[1],name=user[2],hashed_password=user[3],is_active=user[4],strategy_list=[])
    # return models.User(*(user))

def get_user_by_email(db: Session, email: str):
    # return db.query(models.User).filter(models.User.email == email).first()
    query_user = "SELECT * FROM user WHERE email = ?"
    user = cursor.execute(query_user,[email]).fetchone()
    return user

def get_all_user(db: Session, skip: int = 0, limit: int = 100):
    # return db.query(models.User).offset(skip).limit(limit).all()
    users = []
    query_users = "SELECT * FROM user LIMIT ? OFFSET ?"
    for item in cursor.execute(query_users,(limit,skip)):
        user = models.User(id=item[0],email=item[1],name=item[2],hashed_password=item[3],is_active=item[4],strategy_list=[])
        users.append(user)
    return users


# market
def create_market(db: Session, market: schemas.Market):
    db_market = models.Market(name = market.name ,type = market.type)
    db.add(db_market)
    db.commit()
    db.refresh(db_market)
    return db_market

def get_all_market(db:Session, skip: int = 0, limit: int = 100):
    # query_all = "SELECT * FROM market LIMIT {} OFFSET {}"
    query_all = "SELECT * FROM market LIMIT ? OFFSET ?"
    users = []
    for item in cursor.execute(query_all,(limit,skip)):
        print(item)
        user = models.Market(id=item[0],name=item[1],type=item[2])
        users.append(user)
    return users

def get_market_by_name(db: Session, name: int):
    query = "SELECT * FROM market WHERE name = ?"
    market = cursor.execute(query,[name]).fetchone()
    return market

def get_market_by_id(db: Session, id: int):
    query = "SELECT * FROM market WHERE id = ?"
    market = cursor.execute(query,(id))
    return market


# mType
def get_all_mType(db: Session,skip: int = 0, limit: int = 100 ):
    query_all = "SELECT * FROM marketType LIMIT ? OFFSET ?"
    types = []
    for item in cursor.execute(query_all,(limit,skip)):
        type = models.MarketType(id=item[0],name=item[1])
        types.append(type)
    return types

def get_type_by_name(db: Session, name: str):
    query = "SELECT * FROM marketType WHERE name = ?"
    mType = cursor.execute(query,[name]).fetchone()
    return mType

def create_mType(db: Session, type: schemas.MarketTypeBase):
    print(type.name)
    db_mType = models.MarketType(name = type.name)
    db.add(db_mType)
    db.commit()
    db.refresh(db_mType)
    return db_mType