from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    HR = "hr"
    CHIEF_DOCTOR = "chief_doctor"
    DOCTOR = "doctor"
    EMT = "emt"
    STAFF = "staff"


class User(BaseModel):
    id: str | None = None

    discord_id: str | None = None

    username: str

    email: EmailStr

    password: str

    avatar: str | None = None

    role: UserRole = UserRole.STAFF

    verified: bool = False

    active: bool = True

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)
