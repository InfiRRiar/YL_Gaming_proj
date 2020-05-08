from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.projects import Projects

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('download_link', required=True)


def abort_if_projects_not_found(projects_id):
    session = db_session.create_session()
    projects = session.query(Projects).get(projects_id)
    if not projects:
        abort(404, message=f"Projects {projects_id} not found")


class ProjectsResource(Resource):
    def get(self, projects_id):
        abort_if_projects_not_found(projects_id)
        session = db_session.create_session()
        news = session.query(Projects).get(projects_id)
        return jsonify({'news': news.to_dict()})


class ProjectsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        projects = session.query(Projects).all()
        return jsonify({'projects': [item.to_dict() for item in projects]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        proj = Projects(
            title=args['title'],
            content=args['content'],
            download_link=args['download_link'],
        )
        session.add(proj)
        session.commit()
        return jsonify({'success': 'OK'})
