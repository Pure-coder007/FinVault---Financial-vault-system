from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():
    def bcrypt(password: str):
        hashed_password = pwd_context.hash(password)
        return hashed_password
    
    def verify(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    
    
    
    
class PinHash():
    def bcrypt(transaction_pin: str):
        hashed_pin= pwd_context.hash(transaction_pin)
        return hashed_pin
    
    def verify(plain_pin, hashed_pin):
        return pwd_context.verify(plain_pin, hashed_pin)