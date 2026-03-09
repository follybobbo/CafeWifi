from dotenv import load_dotenv
import os
from itsdangerous import URLSafeTimedSerializer
import itsdangerous

load_dotenv()

secret_key = os.environ.get("APP_SECRET_KEY")

serializer = URLSafeTimedSerializer(secret_key, "email-verify")

def make_token(email: str) -> str:
    token = serializer.dumps(email, salt="email-verify")

    return token


def de_serializer(token: str, expiration=3600):
    try:
        email = serializer.loads(token, max_age=3600, salt="email-verify")
        return email
    except itsdangerous.SignatureExpired:
        return None
    except itsdangerous.BadSignature:
        return None