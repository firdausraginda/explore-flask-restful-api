from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy


# initialize restful API
app = Flask(__name__)
api = Api(app)

# initialize SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={name}), views={views}, likes={likes}"

# only create db once 
# db.create_all()

# storing data in memory
names = {
    "tim": {"age": 19, "gender": "male"},
    "bill": {"age": 22, "gender": "female"}
}

# create request parser object
# 'request parser object' will validate the args that received
video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", type=str, help="name of the video is required", required=True)
video_put_args.add_argument(
    "views", type=int, help="views of the video is required", required=True)
video_put_args.add_argument(
    "likes", type=int, help="likes on the video is required", required=True)

videos = {}


def abort_if_id_not_exists(video_id):
    if video_id not in videos:
        abort(404, message="Video id {} is not valid!".format(video_id))


def abort_if_video_exists(video_id):
    if video_id in videos:
        abort(409, message="Video id {} already exists!".format(video_id))


class HelloWorld(Resource):
    def get(self, name):
        # return {"name": f"Hello {name}!"}
        return names[name]

    def post(self):
        return {"data": "Posted"}


class Video(Resource):
    def get(self, video_id):
        abort_if_id_not_exists(video_id)
        return videos[video_id]

    def put(self, video_id):
        abort_if_video_exists(video_id)
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id]

    def delete(self, video_id):
        abort_if_id_not_exists(video_id)
        del videos[video_id]
        return '', 204


# register class as resource
api.add_resource(HelloWorld, "/helloworld/<string:name>")
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)  # `debug=True` to see all the logging, testing purpose
