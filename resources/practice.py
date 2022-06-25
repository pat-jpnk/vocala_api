from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)

from models.set import SetModel
from models.user import UserModel
from models.vocab import VocabModel

# /users/<username>/sets/<string:set_id/practice>

class Practice(Resource):
    parser = reqparse.RequestParser()

    @jwt_required()
    def get(self, username, set_id):
        user_id = UserModel.find_id_by_name(username)

        if user_id and user_id == get_jwt_identity():                                                                     # TODO: better str cmp ?
            if SetModel.user_has_set(set_id, user_id):
                return {"practice": [x.json() for x in VocabModel.find_practice()]} 
            
            else:
                return {"message": "Set is not valid"}, 404

        else: 
            return {"message": "User does not exist"}, 404
    
    @jwt_required()
    def post(self, id):
        # receive practice outcome (vocabulary) (success | failure) (small mistake | big mistake)
        # process outcome, change level and next_date values
        # validate input

        data = Practice.parser.parse_args()


        return {"message": "Practice complete"}, 200
        '''
                {"practice": [
            {
                "id": XXXX,
                "success": bool,
                "error-level": "none" | "small" | "large"
            },
            
            ...
            ]
        }   
        '''