from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entity_model import Base, User, MediaResource, Prediction

engine = create_engine('mysql+pymysql://root:paulorasan@localhost/demo')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


class UserRepository:

    def __init__(self):
        self.session = Session()

    def get_user_by_email(self, email):
        return self.session.query(User).filter(User.email == email).first()

    def add_user(self, user):
        self.session.add(user)
        self.session.commit()

    def get_all(self):
        return self.session.query(User).all()

    def update_user(self):
        self.session.commit()


class MediaResourceRepository:

    def __init__(self):
        self.session = Session()

    def add_resource(self, resource: MediaResource):
        self.session.add(resource)
        self.session.commit()

    def get_resource_by_file_name(self, path):
        return self.session.query(User).filter(MediaResource.file_name == path).first()


class PredictionRepository:

    def __init__(self):
        self.session = Session()

    def add_prediction(self, pred: Prediction):
        self.session.add(pred)
        self.session.commit()

    def find_predictions_by_user(self, user_id):
        return self.session.query(Prediction).filter(Prediction.user_id == user_id).all()


