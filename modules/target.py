from db import db

class TargetModel(db.Model):
    __tablename__ = 'targets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # parent table column
    strategy_id = db.Column(db.Integer, db.ForeignKey('strategies.id'))
    strategy = db.relationship('StrategyModel')

    def __init__(self, name, price,strategy_id):
        self.name = name
        self.price = price
        self.strategy_id = strategy_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()