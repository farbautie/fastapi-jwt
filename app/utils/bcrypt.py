from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"])

def verify_password(password, hashed_password) -> bool:
    return password_context.verify(password, hashed_password)

def get_password_hash(password) -> str:
    return password_context.hash(password)