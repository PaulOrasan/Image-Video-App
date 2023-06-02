from sqlalchemy import String, Column, Integer, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    is_authorized = Column(Boolean, nullable=False, default=False)
    registration_time = Column(DateTime, nullable=False, server_default=func.now())

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __str__(self):
        return f'{self.id} - {self.email}'


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    image_name = Column(String(50))
