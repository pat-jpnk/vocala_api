import string
from flask import jsonify
from flask_restful import Resource, reqparse
from models.user import UserModel
from models.set import SetModel
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt
)

import string
from hmac import compare_digest
from blocklist import BLOCKLIST


'''

jwt flow:

"fresh token" => "refreshed token" => new "fresh token" (pw entry) | new "refresh token" (jwt token refreshed)

'''


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_jwt()['jti']              # jwt id = jti
        BLOCKLIST.add(jti)
        return {"message": "logged out"}, 200


# /login 

class UserLogin(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('username',
                        type=string,
                        required=True,
                        help="required field"       
    )

    parser.add_argument('password',
                        type=string,
                        required=True,
                        help="required field"       
    )

    @classmethod
    def post(cls):
        # get data from parser
        data = cls.parser.parse_args()
        # find user
        user = UserModel.find_by_username(data['username'])
        # check password -> create access token
        if user and compare_digest(user.password,data['password']):
            access_token = create_access_token(sub=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
        else:
            return {"message": "Invalid Credentials"}, 401


# /users

class Users(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('username',
                        type=string,
                        required=True,
                        help="required field"       
    )

    parser.add_argument('password',
                        type=string,
                        required=True,
                        help="required field"       
    )

    parser.add_argument('email',
                        type=string,
                        required=True,
                        help="required field"       
    )


   # @jwt_required
    def get(self):
        return jsonify({"users": [x.json() for x in UserModel.find_all()]})

    @jwt_required(fresh=True)
    def delete(self):
        pass            # TODO: implement

    def post(self):
        data = self.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A User with name '{}' already exists".format(data['username'])}, 400

        user = UserModel(data['username'], data['password'],data['email'])

        # check for duplicate email

        try:
            user.save()
        except:
            return {"message": "Internal error during insertion"}, 500
        
        return user.json(), 201


# /users/<name>

class User(Resource):

    def get(self, username):
        user = UserModel.find_by_username(username)
        if user:
            return user.json()
        else:
            return {"message": 'User not found'}, 404


    @jwt_required
    def delete(self, username):
        if not UserModel.find_by_username(username):
            return {"message": "User does not exists"}
        else:
            user = UserModel.find_by_username(username)   # duplicate TODO: fix

            try:
                user.delete()
            except:
                return {"message": "Internal error during deletion"}, 500

        return user.json()

    @jwt_required
    def put(self, username):
        pass                   # TODO: implement


# /admin

class Admin(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt()
        if not claims['is_admin']:
            return {"message": "Not allowed"}, 401
        return {"data": 13454}

# return error when no token is provided 

class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        user = get_jwt_identity()
        new_token = create_access_token(sub=user, fresh=False)
        return {'access_token': new_token}, 200
