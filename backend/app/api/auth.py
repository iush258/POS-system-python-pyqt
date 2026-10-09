from typing import Annotated
from fastapi import APIRouter , Depends , HTTPException , status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.user import User
from app.database.session import get_db
from app.schemas.auth import LoginRequest , TokenResponse
from app.security.jwt import create_access_token
from app.security.password import verify_password


router = APIRouter(
    prefix= "/api/auth",
    tags=["Authentication"]
)

@router.post(
    "/login",
    response_model=TokenResponse,
)

def login(
        credentials : LoginRequest,
        db:Annotated[Session,Depends(get_db)],
) -> TokenResponse:
    user = db.scalar(
        select(User).where(
            User.email == credentials.email,
            User.is_active.is_(True),
        )   
    )

    if user is None or not verify_password(
        credentials.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="INVALID email or Password",
        )
    token = create_access_token(
        user_id= user.id,
        role = user.role,
    )

    return TokenResponse(
        access_token= token ,
        token_type="bearer",
    )