'''
Vocala api 0.1
'''
from os import environ

from models.user import UserModel
from models.set import SetModel
from models.vocab import VocabModel
from models.vocab_example import VocabExampleModel

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, get_jwt
from db import db
from blocklist import BLOCKLIST
from dotenv import load_dotenv

from resources.user import RefreshToken, User, UserLogin, UserLogout, Users, Admin
from resources.practice import Practice
from resources.set import Sets, Set
from resources.vocab import SetVocab


app = Flask(__name__)
load_dotenv(".env")

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URI")     # TODO: change
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # turn off flask sqlalchemy modification tracker, leave sqlalchemy modification tracker on
app.config['PROPAGATE_EXCEPTIONS'] = True # provide  better error codes from flask extensions

app.secret_key = environ.get("SECRET_KEY")

api = Api(app)


# creates all tables existent in db URI
@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:                   # use other, read from .env / decide if remove, use /login resource instead
        return {"is_admin": True}       # TODO: REPLACE
    else:
        return {"is_admin": False}

def token_in_blocklist(decrypted_token):
    return decrypted_token['jti'] in BLOCKLIST

# invalid token sent
@jwt.invalid_token_loader
def invalid_token_callback():
    return jsonify({
        "message": "token invalid"
    }), 401

# expired token sent
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        "message": "token expired"
    }), 401


# no token sent
@jwt.unauthorized_loader
def unauthorized_token_callback():
    return jsonify({
        "message": "no token received"
    }), 401

# non fresh token sent, fresh token required
@jwt.needs_fresh_token_loader
def fresh_token_callback():
    return jsonify({
        "message": "fresh token required"
    }), 401

# logout user
@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "message": "revoked token received"
    }), 401



# ------ API resources ------

api.add_resource(RefreshToken, '/refresh')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserLogin, '/login')
api.add_resource(Users, '/users')
api.add_resource(User, '/users/<string:username>')
api.add_resource(Sets, '/users/<string:username>/sets')
api.add_resource(Set, '/users/<string:username>/sets/<string:set_id>')
api.add_resource(SetVocab, '/users/<string:username>/sets/<string:set_id>/vocab')
api.add_resource(Practice, '/users/<string:username>/sets/<string:set_id>/practice')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=7799, debug=environ.get("DEBUG"))

