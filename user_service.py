from entity_model import User
from repository_persistence import UserRepository
from passlib.hash import sha256_crypt

class UserService:

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def check_user_credentials(self, email, password):
        user = self.find_user_by_email(email)
        return user is not None and sha256_crypt.verify(password, user.password)

    def register_new_user(self, email, password):
        user = self.find_user_by_email(email)
        if user is not None:
            return None
        user = User(email=email, password=password)
        self.repo.add_user(user)
        return user

    def find_user_by_email(self, email):
        return self.repo.get_user_by_email(email)


    def find_all_users(self):
        return self.repo.get_all()

    def update_authorization(self, email, flag):
        user = self.find_user_by_email(email)
        user.is_authorized = flag
        self.repo.update_user()