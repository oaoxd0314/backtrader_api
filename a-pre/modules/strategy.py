from db import db

class StrategyModel(db.Model):
    __tablename__ = 'strategies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    
    # child table
    # 如果啟用 lazy='dynamic' ,self.targets 將不會是一個 list 而是一個 query builder（為了不讓初始等待時間過長 => 只有當需要使用才會用 self.targets 找到擁有該 Strategy.id 的 targets）
    targets = db.relationship('TargetModel', lazy='dynamic')

    # parent table
    user = db.relationship('UserModel')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    

    def __init__(self, name,user_id):
        self.name = name
        self.user_id = user_id

    def json(self):
        #因為 self.targets 是 query builder 所以要取得符合的全部 item 就要用 .all() 
        return {'name': self.name, 'targets': [item.json() for item in self.targets.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all_by_userID(cls,uid):
        return cls.query.filter_by(user_id=uid).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()