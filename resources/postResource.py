from flask_restful import reqparse, Resource
from models.postModel import PostModel
import datetime

class Post(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', required = True)
    parser.add_argument('content')
    parser.add_argument('author', required=True)

    def get(self, id):
        post = PostModel.find_by_id(id)
        if post:
            return post.json(), 200 
        else:
            return {'message':'Post not found'}, 404

    def delete(self, id):
        post = PostModel.find_by_id(id)
        post.delete_from_db()

    def put(self, id):
        data = Post.parser.parse_args()
        post = PostModel.find_by_id(id)
        if post:
            post.title = data['title']
            post.content = data['content']
        else:
            post = PostModel(data['title'], data['content'], data['author'])
        post.save_to_db()
        return post.json()

class PostList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', required = True)
    parser.add_argument('content')

    def get(self):
        return {'posts': list(map(lambda x: x.json(), PostModel.query.all()))}

    def post(self):
        data = Post.parser.parse_args()
        post = PostModel(data['title'], data['content'], data['author'])
        post.save_to_db()
        return post.json(), 201
    
