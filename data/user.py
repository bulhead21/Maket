import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from .db_session import SqlAlchemyBase
from sqlalchemy import  DateTime


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                    primary_key=True, unique=True)

    name = sqlalchemy.Column(sqlalchemy.String)

    surname = sqlalchemy.Column(sqlalchemy.String)

    email = sqlalchemy.Column(sqlalchemy.String, unique=True)

    phone_num = sqlalchemy.Column(sqlalchemy.String, unique=True)

    password = sqlalchemy.Column(sqlalchemy.String)

    progress = sqlalchemy.Column(sqlalchemy.Integer)

    favourite_routes = sqlalchemy.Column(sqlalchemy.JSON, default=lambda: {
    f"cul_{i}.fav": False for i in range(1, 7)  # 6 маршрутов
})

    completed_routes = sqlalchemy.Column(sqlalchemy.JSON, default=lambda: {
    f"cul_{i}": False for i in range(1, 7)  # 6 маршрутов
})
    
    avatar = sqlalchemy.Column(sqlalchemy.String)
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Route(SqlAlchemyBase):
    __tablename__ = 'routes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                        primary_key=True, unique=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.Text)
    image_url = sqlalchemy.Column(sqlalchemy.String)
    duration = sqlalchemy.Column(sqlalchemy.String)
    difficulty = sqlalchemy.Column(sqlalchemy.String)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow)
