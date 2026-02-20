import jwt
import datetime


class JWTHelper:
    _SECRET_KEY = "THERE WAS A maN, HiS Name ** WA5 T1m"
    _ALGORITHM = "HS256"

    @staticmethod
    def create_token(email):
        """Generates a token that expires in 30 minutes"""
        payload = {
            "user_email": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=45),
            "iat": datetime.datetime.utcnow(),
        }
        # The server signs the data using the SECRET_KEY
        token = jwt.encode(payload, JWTHelper._SECRET_KEY, algorithm=JWTHelper._ALGORITHM)
        return token

    @staticmethod
    def verify_token(token):
        """Verifies the given json web token without querying the database"""
        try:
            # If the token was tampered with or expired, this raises an error
            decoded_payload = jwt.decode(token, JWTHelper._SECRET_KEY, algorithms=[JWTHelper._ALGORITHM])
            return decoded_payload
        except jwt.ExpiredSignatureError:
            return -1
        except jwt.InvalidTokenError:
            return -1
