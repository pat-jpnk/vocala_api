from db import db
from models.set import SetModel

# TODO: add all relationships

class UserModel(db.Model):

    __tablename__ = 'vc_users'         ## pg table name

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))                      # change to sensible value
    password = db.Column(db.String(80))
    email = db.Column(db.String(80))
    
    sets = db.relationship("SetModel", order_by=SetModel.id, back_populates="vc_users")


    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
    
    def json(self):
        return {"username": self.username, "password": self.password ,"email": self.email}
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_by_username(cls, name):
        return cls.query.filter_by(username=name).first()

    @classmethod
    def find_name_by_id(cls, user_id):
        return cls.query(cls.username).filter_by(id=user_id).first()

    @classmethod
    def find_id_by_name(cls, name):
        return cls.query(cls.id).filter_by(username=name).first()

    @classmethod
    def find_all(cls):
        return cls.query().all()