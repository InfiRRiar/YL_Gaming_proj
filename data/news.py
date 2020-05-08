import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class News(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # заголвок новости
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # основной текст новости
    author = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # автор новости
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,  # дата создания
                                     default=datetime.datetime.now)
