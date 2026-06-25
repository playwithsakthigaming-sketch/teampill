from datetime import datetime,timedelta

from jose import jwt

from app.config import settings

ALGORITHM="HS256"

ACCESS_TOKEN_EXPIRE=15

REFRESH_TOKEN_EXPIRE=30


def create_access_token(data:dict):

    payload=data.copy()

    payload["exp"]=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE)

    return jwt.encode(payload,settings.JWT_SECRET,algorithm=ALGORITHM)


def create_refresh_token(data:dict):

    payload=data.copy()

    payload["exp"]=datetime.utcnow()+timedelta(days=REFRESH_TOKEN_EXPIRE)

    return jwt.encode(payload,settings.JWT_SECRET,algorithm=ALGORITHM)
