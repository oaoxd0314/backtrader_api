from sqlalchemy.orm import Session, query
from sqlalchemy.sql.functions import mode
from core.database import cursor,connection
from distutils.util import strtobool
from core import models,schemas

# user
def get_user_by_id(db: Session, id: int):
    query_user = "SELECT * FROM user WHERE id = ?"
    db_user = cursor.execute(query_user,[id]).fetchone()
    
    if(db_user):
        return models.User(id=db_user[0],email=db_user[1],name=db_user[2],hashed_password=db_user[3],is_active=db_user[4],strategy_list=[])

def get_user_by_email(db: Session, email: str):
    # return db.query(models.User).filter(models.User.email == email).first()
    query_user = "SELECT * FROM user WHERE email = ?"
    db_user = cursor.execute(query_user,[email]).fetchone()
    if(db_user):
        return models.User(id=db_user[0],email=db_user[1],name=db_user[2],hashed_password=db_user[3],is_active=db_user[4],strategy_list=[])

def get_all_user(db: Session, skip: int = 0, limit: int = 100):
    # return db.query(models.User).offset(skip).limit(limit).all()
    users = []
    query_users = "SELECT * FROM user LIMIT ? OFFSET ?"
    for item in cursor.execute(query_users,(limit,skip)):
        user = models.User(id=item[0],email=item[1],name=item[2],hashed_password=item[3],is_active=item[4],strategy_list=[])
        users.append(user)
    return users
    
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    query = "INSERT INTO user (name,email,hashed_password) VALUES (?,?,?)"
    cursor.execute(query,[user.name,user.email,fake_hashed_password])
    connection.commit()
    
    db_user = get_user_by_email(db,user.email)
    return models.User(id=db_user.id, name=db_user.name, email=db_user.email,is_active=db_user.is_active)

def delete_user(db: Session,user:schemas.User):
    query = "DELETE FROM user WHERE id = ? AND email = ? AND name = ?"
    cursor.execute(query,[user.id,user.email,user.name])
    connection.commit()

    return user

def update_user(db: Session,user:schemas.User):
    query = "UPDATE user SET name = ? ,is_active = ? WHERE id = ? AND email = ?"

    cursor.execute(query,[user.name,user.is_active,user.id,user.email])
    connection.commit()

    return get_user_by_id(db,id=user.id)


# market
def get_all_market(db:Session, skip: int = 0, limit: int = 100):
    # query_all = "SELECT * FROM market LIMIT {} OFFSET {}"
    query_all = "SELECT * FROM market LIMIT ? OFFSET ?"
    users = []
    for item in cursor.execute(query_all,(limit,skip)):
        user = models.Market(id=item[0],name=item[1],type=item[2])
        users.append(user)
    return users

def get_market_by_name(db: Session, name: int):
    query = "SELECT * FROM market WHERE name = ?"
    db_market = cursor.execute(query,[name]).fetchone()

    if(db_market):
        return models.Market(id=db_market[0],name=db_market[1],type=db_market[2])
    

def get_market_by_id(db: Session, id: int):
    query = "SELECT * FROM market WHERE id = ?"
    db_market = cursor.execute(query,[id]).fetchone()

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
