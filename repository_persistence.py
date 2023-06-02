from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entity_model import Base, User

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


repo = UserRepository()
print(repo.get_user_by_email('abba'))