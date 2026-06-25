from fastapi import Depends, HTTPException, status

from fastapi.security import HTTPAuthorizationCredentials

from fastapi.security import HTTPBearer

from jose import JWTError

from jose import jwt

from app.config import settings

from app.database.users import get_user_by_id

security = HTTPBearer()

ALGORITHM = "HS256"


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired or invalid"
        )

    user = await get_user_by_id(user_id)

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


def require_roles(*roles):

    async def checker(user=Depends(get_current_user)):

        if user["role"] not in roles:

            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )

        return user

    return checker
