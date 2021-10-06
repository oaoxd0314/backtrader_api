from flask_restful import Resource
from modules.strategy import StrategyModel


class Strategy(Resource):
    def get(self, name):
        Strategy = StrategyModel.find_by_name(name)
        if Strategy:
            return Strategy.json()
        return {'message': 'Strategy not found'}, 404

    def post(self, name):
        if StrategyModel.find_by_name(name):
            return {'message': "A Strategy with name '{}' already exists.".format(name)}, 400

        Strategy = StrategyModel(name)
        try:
            Strategy.save_to_db()
        except:
            return {"message": "An error occurred creating the Strategy."}, 500

        return Strategy.json(), 201

    def delete(self, name):
        Strategy = StrategyModel.find_by_name(name)
        if Strategy:
            Strategy.delete_from_db()

        return {'message': 'Strategy deleted'}


class StrategyList(Resource):
    def get(self):
        # return {'Strategies': list(map(lambda x: x.json(), StrategyModel.query.all()))}
        return {'Strategies' : [item.json() for item in StrategyModel.query.all()]}