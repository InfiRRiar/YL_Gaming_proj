import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    vk_id = sqlalchemy.Column(sqlalchemy.String, default=None)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    is_submit = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    submit_code = sqlalchemy.Column(sqlalchemy.String)
    added_games = sqlalchemy.Column(sqlalchemy.String, default="")
    is_developer = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
