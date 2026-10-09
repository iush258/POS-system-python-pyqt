from collections.abc import Callable, Generator
from typing import Annotated, Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.user import User, UserRole
from app.database.session import get_db
from app.security.jwt import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
)

DatabaseSession = Annotated[
    Session,
    Depends(get_db),
]


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: DatabaseSession,
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        subject = payload.get("sub")

        if subject is None:
            raise credentials_exception

        user_id = int(subject)

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError):
        raise credentials_exception from None

    user = db.scalar(
        select(User).where(
            User.id == user_id,
            User.is_active.is_(True),
        )
    )

    if user is None:
        raise credentials_exception

    return user


CurrentUser = Annotated[
    User,
    Depends(get_current_user),
]


def require_roles(
    *allowed_roles: UserRole,
) -> Callable[..., User]:
    def role_dependency(
        current_user: CurrentUser,
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return current_user

    return role_dependency


AdminUser = Annotated[
    User,
    Depends(require_roles(UserRole.ADMIN)),
]


CashierOrAdminUser = Annotated[
    User,
    Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.CASHIER,
        )
    ),
]