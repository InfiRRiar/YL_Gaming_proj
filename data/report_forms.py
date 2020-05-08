import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class ReportForms(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'reports'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # заголовок обращеня
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # текст
    author = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # автор
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)  # дата создания
