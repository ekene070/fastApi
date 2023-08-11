from passlib.context import CryptContext


class Hash():
    def encrypt_password(password: str):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash(password)
        return hashed_password
