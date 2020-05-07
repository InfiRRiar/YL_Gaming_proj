from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.news import News

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('author', required=True)


def abort_if_news_not_found(news_id):
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news:
        abort(404, message=f"News {news_id} not found")


class NewsResource(Resource):
    def get(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        return jsonify({'news': news.to_dict()})


class NewsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(News)
        return jsonify({'news': [item.to_dict(only=('title', 'content', 'author', 'id')) for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        news = News(
            title=args['title'],
            content=args['content'],
            author=args['author'],
        )
        session.add(news)
        session.commit()
        return jsonify({'success': 'OK'})
