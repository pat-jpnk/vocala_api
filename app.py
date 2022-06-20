'''
Vocala api 0.1
'''

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, jwt_required 
from db import db

from security import authenticate, identity
from resources.user import User, Users, Sets, Set, Practice


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:://aws-example.com'       # TODO: change
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # turn off flask sqlalchemy modification tracker, leave sqlalchemy modification tracker on
app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = "ABCDEFG"
api = Api(app)

'''
# creates all tables existent in db URI
@app.before_first_request
def create_tables():
    db.create_all()
'''

jwt = JWT(app, authenticate, identity)


# ------ API resources ------

api.add_resource(Users, '/users')
api.add_resource(User, '/users/<string:username>')
api.add_resource(Sets, '/users/<string:username>/sets')
api.add_resource(Set, '/users/<string:username>/sets/<string:id>')
api.add_resource(Practice, '/users/<string:username>/sets/<string:id>/practice')


if __name__ == '__main__':
 #   db.init_app(app)
    app.run(port=7799, debug=True)      # TODO: set debug false

