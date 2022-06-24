from db import db


class VocabExampleModel(db.Model):
    
    __tablename__ = 'vc_usage_examples'         
    
    id = db.Column(db.Integer, primary_key=True)
    example = db.Column(db.String)
    vocab_id = db.Column(db.Integer, db.ForeignKey("vc_vocabularies.id"))


    def __init__(self, id, example, vocab_id):
        self.id = id,
        self.example = example
        self.vocab_id = vocab_id

    def json(self):
        return {"id": self.id, "example": self.example, "vocab_id": self.vocab_id}
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_by_vocab_id(cls, vocab_id):
        return cls.query.filter_by(id=vocab_id).all()

