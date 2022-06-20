import string
from flask_restful import Resource, reqparse
from models.user import UserModel
from models.set import SetModel
from flask_jwt import jwt_required

# /users/<name>

class User(Resource):

    def get(self, name):
        user = UserModel.find_by_username(name)
        if user:
            return {"user": name}  
        else:
            return {"message": 'User not found'}, 404


    @jwt_required
    def delete(self, name):
        if not UserModel.find_by_username(name):
            return {"message": "User does not exists"}
        else:
            user = UserModel.find_by_username(name)   # duplicate

            try:
                user.delete()
            except:
                return {"message": "Internal error during deletion"}, 500

        return user.json()


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

    
    def post(self):
        if UserModel.find_by_username(data['username']):
            return {"message": "A User with name '{}' already exists".format(name)}, 400
        
        data = User.parser.parse_args()
        user = UserModel(data['username'], data['password'],data['email'])

        try:
            user.save()
        except:
            return {"message": "Internal error during insertion"}, 500
        
        return user.json(), 201


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
            return {'sets': list(map(lambda x: x.json(), SetModel.find_by_user_id(user_id)))} 

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


# /users/<name>/sets/<string:id/practice>

class Practice(Resource):
    @jwt_required
    def get(self, id):
        pass                          # TODO: implement