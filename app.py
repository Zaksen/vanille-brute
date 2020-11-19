from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from resources.postResource import Post, PostList
from resources.userResource import UserRegister, User

app = Flask(__name__)
app.secret_key = 'zak'
api = Api(app)
jwt = JWT(app, authenticate, identity) # /auth

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Post, '/post/<int:id>')
api.add_resource(PostList, '/posts')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<string:username>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)