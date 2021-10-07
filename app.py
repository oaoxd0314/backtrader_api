import os
from  flask_restful import Api
from flask import Flask,request,jsonify
# from resources.stock import Stock
from datetime import timedelta
from security import authenticate, identity as identity_function
from resources.user import UserRegister,UserList
from resources.strategy import Strategy,StrategyList
from resources.target import Target,TargetList
from flask_jwt import JWT
from db import db

app = Flask(__name__)
app.secret_key = 'Chris'
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800) # token expire time = half an hour
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///data.db') # os.environ.get('DATABASE_URL' 是抓取 heroku 上的 PostgresSql 位址 所以我們可以在第二個 param 放入預設的 sqlite 位址（在本地端時啟用）
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api =Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity_function)

api.add_resource(Strategy,'/strategy/<string:name>')
api.add_resource(Target,'/target/<string:name>')
api.add_resource(TargetList,'/targets')
api.add_resource(UserRegister,'/register')
api.add_resource(UserList,'/admin/allUser')
api.add_resource(StrategyList,'/allStrategy')

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
    })


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)