from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from app.config import get_settings
from app.database.models.user import UserRole


settings = get_settings()

ALGORITHM = "HS256"


def create_access_token(
    user_id: int,
    role: UserRole,
) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload: dict[str, Any] = {
        "sub": str(user_id),
        "role": role.value,
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=[ALGORITHM],
    )