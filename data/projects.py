import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Projects(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'projects'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # заголовок проекта
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # кратко описание
    download_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # ссылка на скачивание
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)  # дата создания
