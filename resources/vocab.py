from flask import jsonify
from flask_restful import Resource, reqparse
from models.user import UserModel
from models.set import SetModel
from flask_jwt_extended import (
    jwt_required
)

# /users/<name>/sets/<string:id/vocab

# TODO: paginate, filter, sort

class SetVocab(Resource):
    @jwt_required
    def get(self, username, set_id):
        user_id = UserModel.find_id_by_name(username)

        if user_id:
            set = SetModel.find_by_id(set_id)
            if set:
                return {"vocab": [x.json() for x in SetModel.find_by_user_id(user_id).vocab]}
            else:
                return {"message": "Set does not exist"}, 404
        else:
            return {"message": "User does not exist"}, 404

