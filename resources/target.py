from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from modules.target import TargetModel

class Target(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float ,
        required=True ,
        help = "this field cannot be left blank"
    )
    parser.add_argument('strategy_id',
        type=int ,
        required=True ,
        help = "Every target need a strategy id"
    )

    @jwt_required()
    def get(self,name):
        target = TargetModel.find_by_name(name)
        if target:
            return target.json()
        return {'message': f"target {name} doesn't exist"},404

    def post(self,name):
        if TargetModel.find_by_name(name):
            return {'message' : f'target {name} is already exist'}, 400

        data = Target.parser.parse_args()
        target = TargetModel(name,**data)

        try:
            target.save_to_db()
        except:
            return {'message':'insert fail'},500

        return target.json() , 201
    
    def delete(self,name):
        target = TargetModel.find_by_name(name)

        if target:
            target.delete_from_db()

        return {'message':'target delete'}
            
    def put(self,name):
        data = Target.parser.parse_args()
        target = TargetModel.find_by_name(name)

        if target is None:
            target = TargetModel(name,**data)
        else :
            target.price = data['price']
            target.strategy_id = data['strategy_id']

        
        target.save_to_db()

        return target.json()

class TargetList(Resource):
    def get(self):
        # return {'targets': list(map(lambda x : x.json() , targetModel.query.all()))}
        return {'targets': [x.json() for x in TargetModel.query.all()]}