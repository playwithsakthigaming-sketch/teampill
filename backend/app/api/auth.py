from datetime import UTC, datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.schemas.user import RegisterSchema
from app.schemas.user import LoginSchema
from app.schemas.token import TokenResponse
from app.auth.security import hash_password
from app.auth.security import verify_password
from app.auth.jwt import create_access_token
from app.auth.jwt import create_refresh_token
from app.database.users import create_user
from app.database.users import get_user_by_email
from app.database.users import update_refresh_token
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(
    payload: RegisterSchema
):

    existing = await get_user_by_email(payload.email)

    if existing:

        raise HTTPException(
            status_code=409,
            detail="Email already registered."
        )

    password_hash = hash_password(
        payload.password
    )

    document = {

        "username": payload.username,

        "email": payload.email,

        "password": password_hash,

        "role": "staff",

        "verified": False,

        "active": True,

        "discord_id": None,

        "avatar": None,

        "created_at": datetime.now(UTC),

        "updated_at": datetime.now(UTC)

    }

    user_id = await create_user(
        document
    )

    access_token = create_access_token(
        {
            "sub": user_id,
            "role": "staff"
        }
    )

    refresh_token = create_refresh_token(
        {
            "sub": user_id
        }
    )

    await update_refresh_token(
        user_id,
        refresh_token
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post(
    "/login",
    response_model=TokenResponse
)
async def login(
    payload: LoginSchema
):

    user = await get_user_by_email(
        payload.email
    )

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    if not verify_password(
        payload.password,
        user["password"]
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    if not user["active"]:

        raise HTTPException(
            status_code=403,
            detail="Account disabled."
        )

    access_token = create_access_token(
        {
            "sub": str(user["_id"]),
            "role": user["role"]
        }
    )

    refresh_token = create_refresh_token(
        {
            "sub": str(user["_id"])
        }
    )

    await update_refresh_token(
        str(user["_id"]),
        refresh_token
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.get(
    "/me"
)
async def current_user(
    user=Depends(
        get_current_user
    )
):

    return {

        "id": str(
            user["_id"]
        ),

        "username": user["username"],

        "email": user["email"],

        "role": user["role"],

        "verified": user["verified"],

        "discord_id": user["discord_id"],

        "avatar": user["avatar"]

    }
