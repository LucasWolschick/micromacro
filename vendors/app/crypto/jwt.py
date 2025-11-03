from datetime import datetime, timedelta
from jose import jwt, JWTError

from app.settings import settings
from app.exceptions import NotAuthenticatedException


def issue(vendor_id: int, duration: timedelta) -> str:
    token = jwt.encode(
        {"sub": vendor_id, "exp": datetime.now() + duration},
        settings.jwt_secret,
        algorithm="HS256",
    )
    return token


def decode_vendor_id(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
    except JWTError:
        raise NotAuthenticatedException()

    return payload["sub"]
