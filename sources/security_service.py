from cryptography.fernet import Fernet


class SecurityService:

    def __init__(self):
        fernet_key = Fernet.generate_key()
        self.cipher = Fernet(fernet_key)

    def encrypt_resource(self, name: str):
        return self.cipher.encrypt(name.encode()).decode()

    def decrypt_resource(self, name: str):
        return self.cipher.decrypt(name.encode())

