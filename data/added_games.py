import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class AddedGames(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'added_games'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    project_name = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    username = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
