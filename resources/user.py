import imp
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
        #return jsonify(UserModel.find_all())

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

# /users/<name>/sets

class Sets(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('setname',
                        type=string,
                        required=True,
                        help="required field"       
    )

    parser.add_argument('user_id',
                        type=string,
                        required=True,
                        help="required field"       
    )

    def get(self, username):
        
        user_id = UserModel.find_id_by_name(username)

        if user_id:
            return {"sets": [x.json() for x in SetModel.find_by_user_id(user_id)]} 

        else: 
            return {"message": "User does not exist"}, 404

    @jwt_required
    def post(self, username):
        
        data = User.parser.parse_args()
        if not SetModel.find_by_setname(data['setname']): 
            if not UserModel.find_by_username(username):
                set = SetModel(data['setname'], data['user_id'])
                
                try:
                    set.save()
                except:
                    return {"message": "Internal error during insertion"}, 500
            
                return set.json(), 201

            else:
                return {"message": "User is not valid"}
        else:
            return {"message": "Set with name {} already exists".format(data['setname'])}


# /users/<name>/sets/<string:id>

class Set(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('set_id',
                        type=string,
                        required=True,
                        help="required field"       
    )

    @jwt_required
    def get(self, username, set_id):
        user_id = UserModel.find_id_by_name(username)

        if user_id:
            set = SetModel.find_by_id(set_id)
            if set:
                return set.json()
            else:
                return {"message": "Set does not exist"}, 404
        else:
            return {"message": "User does not exist"}, 404

    @jwt_required
    def put(self, username, set_id):
        pass                                # TODO: implement

    @jwt_required
    def delete(self, username, set_id):
        user_id = UserModel.find_id_by_name(username)

        if user_id:
            set = SetModel.find_by_id(set_id)
            if set:
                try:
                    set.delete()
                except:
                    return {"message": "Internal error during deletion"}, 500
            else:
                return {"message": "Set does not exist"}, 404
        else:
            return {"message": "User does not exist"}, 404



# /users/<name>/sets/<string:id/vocab

# paginate, filter, sort

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





# /users/<name>/sets/<string:id/practice>

class Practice(Resource):
    @jwt_required
    def get(self, id):
        pass                          # TODO: implement

        # return X vocabularies in set for which next_date <= today
    
    @jwt_required
    def post(self, id):
        # receive practice outcome (vocabulary) (success | failure) (small mistake | big mistake)
        # process outcome, change level and next_date values
        # validate input
        pass



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
