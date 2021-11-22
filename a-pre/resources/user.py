from os import name
import sqlite3
from sqlite3.dbapi2 import connect
from flask_restful import Resource,reqparse
from modules.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="this field 'username' cannot be blank"    
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="this field 'password' cannot be blank"    
    )

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message":f"{data['username']} has been resgited"},400
        
        user = UserModel(**data)
        user.save_to_db()

        return{"message" : "User created sus"}, 201
    
    def get(self):
        conn = sqlite3.connect('data.db')
        cursor =conn.cursor()
        select_query = "SELECT * FROM users"

        memberlist  = cursor.execute(select_query)
        
        result = {member[0] : {'name':member[1],'password':member[2]} for member in memberlist}

        conn.close()

        return result, 201

class UserList(Resource):
    def get(self):
        # return {'targets': list(map(lambda x : x.json() , targetModel.query.all()))}
        return {'users': [x.json() for x in UserModel.query.all()]}