from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
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
        return f"Video(name={self.name}), views={self.views}, likes={self.likes}"


# only create db once 
# db.create_all()

# create request parser object
# 'request parser object' will validate the args that received
video_post_args = reqparse.RequestParser()
video_post_args.add_argument(
    "name", type=str, help="name of the video is required", required=True)
video_post_args.add_argument(
    "views", type=int, help="views of the video is required", required=True)
video_post_args.add_argument(
    "likes", type=int, help="likes on the video is required", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument(
    "name", type=str)
video_update_args.add_argument(
    "views", type=int)
video_update_args.add_argument(
    "likes", type=int)


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id=None):
        if not video_id:
            result = VideoModel.query.all()
        else:
            result = VideoModel.query.filter_by(id=video_id).first()
            if not result:
                abort(404, message="id doesn't exists!")
            
        return result

    @marshal_with(resource_fields)
    def post(self, video_id):
        args = video_post_args.parse_args()
        
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="id already exists")

        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()

        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="id not found, can't update")
        
        for key, value in args.items():
            if value:
                setattr(result, key, value)

        db.session.commit()

        return result

    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(409, message="id is not exists")
        
        db.session.delete(result)
        db.session.commit()
        
        return '', 204


# register class as resource
api.add_resource(Video, "/video", "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)  # `debug=True` to see all the logging, testing purpose
