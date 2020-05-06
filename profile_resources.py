from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.users import User

parser = reqparse.RequestParser()
parser.add_argument('username', required=True)
parser.add_argument('vk_id', required=True)
parser.add_argument('is_submit', required=True)
parser.add_argument('submit_code', required=True)
parser.add_argument('is_developer', required=True)
parser.add_argument('password', required=True)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, username):
        session = db_session.create_session()
        user = session.query(User).filter(User.username == username).first()
        abort_if_user_not_found(user.id)
        return jsonify({"user": user.to_dict()})


class UserListResource(Resource):
    def post(self):
        pass
