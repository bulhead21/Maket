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
    def get_total_hours(self, db_sess):
        if not self.completed_routes:
            return 0

        # Получаем ID завершенных маршрутов (где значение True)
        completed_ids = [int(route_id.replace('cul_', '')) 
                        for route_id, completed in self.completed_routes.items() 
                        if completed]

        # Запрашиваем длительность этих маршрутов из БД
        routes = db_sess.query(Route.duration).filter(Route.id.in_(completed_ids)).all()
        
        # Суммируем часы (предполагаем, что duration в формате "2 часа")
        total_hours = 0
        for (duration,) in routes:
            if duration:
                hours = duration  # Извлекаем число из строки "2 часа"
                total_hours += hours

        return total_hours
    def get_total_photos(self):
        if not self.completed_routes:
            return 0
        # Считаем количество завершённых маршрутов (True в completed_routes)
        return sum(1 for completed in self.completed_routes.values() if completed)

class Route(SqlAlchemyBase):
    __tablename__ = 'routes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                        primary_key=True, unique=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.Text)
    image_url = sqlalchemy.Column(sqlalchemy.String)
    duration = sqlalchemy.Column(sqlalchemy.FLOAT)
    difficulty = sqlalchemy.Column(sqlalchemy.String)
