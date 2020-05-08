from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.report_forms import ReportForms

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('author', required=True)


def abort_if_report_not_found(report_id):
    session = db_session.create_session()
    report = session.query(ReportForms).get(report_id)
    if not report:
        abort(404, message=f"News {report_id} not found")


class ReportsResource(Resource):
    def get(self, report_id):
        abort_if_report_not_found(report_id)
        session = db_session.create_session()
        report = session.query(ReportForms).get(report_id)
        print(report)
        return jsonify({'report': report.to_dict()})

    def delete(self, report_id):
        abort_if_report_not_found(report_id)
        session = db_session.create_session()
        report = session.query(ReportForms).get(report_id)
        session.delete(report)
        session.commit()
        return jsonify({'success': 'OK'})


class ReportsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(ReportForms)
        return jsonify({'reports': [item.to_dict() for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        report = ReportForms(
            title=args['title'],
            content=args['content'],
            author=args['author'],
        )
        session.add(report)
        session.commit()
        return jsonify({'success': 'OK'})
