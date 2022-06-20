from db import db

class VocabModel(db.Model):
    
    __tablename__ = 'vc_vocabularies'

    id = db.Column(db.Integer, primary_key=True)
    set_id = db.Column(db.Integer)
    native = db.Column(db.String(50))                   # change to sensible value
    foreign = db.Column(db.String(50))
    next_date = db.Column(db.Date)
    level = db.Column(db.Integer)
    description = db.Column(db.String(50))
    
    def __init__(self, native, foreign, set_id, next_date, description):
        self.native = native,
        self.foreign = foreign,
        self.set_id = set_id,
        self.level = 1,              # TODO: set sensible
        self.next_date = "",        # TODO: fix
        self.description = description

    def json(self):
        return {"native": self.native, "foreign": self.foreign, "set_id": self.set_id, "level": self.level, "description": self.description}
        

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    