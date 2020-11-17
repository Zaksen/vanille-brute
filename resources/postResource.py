from flask_restful import reqparse, Resource
from models.postModel import PostModel

class Post(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', required = True)
    parser.add_argument('content')

    def get(self, _id):
        post = PostModel.find_by_id(_id)
        return post.json(), 200 if post else {'message':'Post not found'}, 404

    def delete(self, _id):
        post = PostModel.find_by_id(_id)
        post.delete_from_db()

    def put(self, _id):
        data = Post.parser.parse_args()
        post = PostModel.find_by_id(_id)
        if post:
            post.title = data['title']
            post.content = data['content']
        else:
            post = PostModel(data['title'], data['content'])
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
        post = PostModel(data['title'], data['content'])
        post.save_to_db()
        return post.json(), 201
    
