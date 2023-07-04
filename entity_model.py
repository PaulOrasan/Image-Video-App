from sqlalchemy import String, Column, Integer, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(500), nullable=False)
    is_authorized = Column(Boolean, nullable=False, default=False)
    registration_time = Column(DateTime, nullable=False, server_default=func.now())

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __str__(self):
        return f'{self.id} - {self.email}'


class MediaResource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    file_name = Column(String(50), nullable=False)
    is_image = Column(Boolean, nullable=False, default=True)

    def __init__(self, **kwargs):
        super(MediaResource, self).__init__(**kwargs)


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    source_image_id = Column(Integer, ForeignKey('resources.id'))
    output_video_id = Column(Integer, ForeignKey('resources.id'))
    request_time = Column(DateTime, nullable=False, server_default=func.now())
    prompt = Column(String(50), nullable=False)
    negative_prompt = Column(String(50), default="")
    field_x = Column(Integer, nullable=False)
    field_y = Column(Integer, nullable=False)
    t0 = Column(Integer, nullable=False)
    t1 = Column(Integer, nullable=False)
    seed = Column(Integer, nullable=False)

    def __init__(self, **kwargs):
        super(Prediction, self).__init__(**kwargs)
