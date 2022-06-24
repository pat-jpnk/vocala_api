from db import db
from datetime import date

class VocabModel(db.Model):
    
    __tablename__ = 'vc_vocabularies'

    id = db.Column(db.Integer, primary_key=True)
    set_id = db.Column(db.Integer, db.ForeignKey('vc_sets.id'))
    native = db.Column(db.String(50))                   # change to sensible value
    foreign = db.Column(db.String(50))
    next_date = db.Column(db.Date)
    level = db.Column(db.Integer)
    description = db.Column(db.String(50), nullable=True)
    
    examples = db.relationship("VocabExampleModel", backref="vocab")

    def __init__(self, native, foreign, set_id, description):
        self.native = native
        self.foreign = foreign
        self.set_id = set_id
        self.level = 1
        self.next_date = db.current_date()     # tell sql to let DB engine calculate DATE value, removing proccess from application level
        self.description = description

    def json(self):
        return {"native": self.native, "foreign": self.foreign, "set_id": self.set_id, "level": self.level, "description": self.description}
        

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    
    @classmethod
    def find_practice(cls, set_id):
        return cls.query.filter_by(set_id=set_id).filter(cls.next_date <= date.today()).limit(10).all()