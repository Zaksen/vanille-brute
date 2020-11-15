from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity


app = Flask(__name__)
app.secret_key = 'zak'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth
posts = []

class Post(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', required = True)
    parser.add_argument('content')

    def get(self, id):
        post = next(filter(lambda x: x['id'] == id, posts), None)
        return {'post': post}, 200 if post else 404

    def post(self, id = None):
        data = Post.parser.parse_args()
        new_id = 1 if not posts else posts[-1]['id'] + 1
        new_post = {
            'id' : new_id,
            'title' : data['title'],
            'content' : data['content']
        }
        posts.append(new_post)
        return new_post, 201

    def delete(self, id):
        global posts
        posts = list(filter(lambda x: x['id'] != id, posts))
        return {'message': 'Post deleted'}

    def put(self, id):
        data = Post.parser.parse_args()
        post = next(filter(lambda x: x['id'] == id, posts), None)
        if post is None:
            new_id = 1 if not posts else posts[-1]['id'] + 1
            new_post = {
            'id' : new_id,
            'title' : data['title'],
            'content' : data['content']
            }
            posts.append(new_post)
        else:
            post.update(data)
        return post


class PostList(Resource):
    def get(self):
        return {'posts': posts}
    
api.add_resource(Post, '/post/<int:id>', '/post/')
api.add_resource(PostList, '/posts')


app.run(port=5000)