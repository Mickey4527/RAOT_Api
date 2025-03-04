from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["scrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """
        ตรวจสอบรหัสผ่าน
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
        สร้างรหัสผ่าน
    """
    return pwd_context.hash(password)

def random_password():
    """
        สร้างรหัสผ่านสุ่ม
    """
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))