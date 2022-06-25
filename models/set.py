from db import db

class SetModel(db.Model):

    __tablename__ = 'vc_sets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("vc_users.id"))
    setname = db.Column(db.String(50))                   # change to sensible value

    vocab = db.relationship("VocabModel", backref="set")


    def __init__(self, setname, user_id):
        self.setname = setname
        self.user_id = user_id
    
    def json(self):
        return {"id": self.id, "user_id": self.user_id ,"setname": self.setname}

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_user_id(cls, id):
        return cls.query.filter_by(user_id=id).all()


    @classmethod
    def find_by_setname(cls, name):
        return cls.query.filter_by(setname=name).first()

    @classmethod
    def find_by_id(cls, set_id):
        return cls.query.filter_by(id=set_id).first();

    @classmethod
    def user_has_set(cls, set_id, user_id):
        set = cls.query.filter_by(id = set_id).first()
        return set.user_id == user_id