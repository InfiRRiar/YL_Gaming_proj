from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.added_games import AddedGames

parser = reqparse.RequestParser()
parser.add_argument('project_name', required=True)
parser.add_argument('username', required=True)


def abort_if_games_not_found(game_id):
    session = db_session.create_session()
    projects = session.query(AddedGames).get(game_id)
    if not projects:
        abort(404, message=f"Projects {game_id} not found")


class AddedGamesResource(Resource):
    def delete(self, game_id):
        abort_if_games_not_found(game_id)
        session = db_session.create_session()
        news = session.query(AddedGames).get(game_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class AddedGamesListResource(Resource):
    def get(self):
        session = db_session.create_session()
        games = session.query(AddedGames).all()
        return jsonify({'games': [item.to_dict() for item in games]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        games = AddedGames(
            project_name=args['project_name'],
            username=args['username'],
        )
        session.add(games)
        session.commit()
        return jsonify({'success': 'OK'})
