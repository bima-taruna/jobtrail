from passlib.context import CryptContext

pass_context = CryptContext(
    schemes=['bcrypt']
)

def generate_pass_hash(password:str)->str:
    hash = pass_context.hash(password)
    return hash

def verify_password(password:str, hash: str) -> bool:
    return pass_context.verify(password, hash)