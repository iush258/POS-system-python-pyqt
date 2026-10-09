from fastapi import APIRouter

from app.security.dependencies import AdminUser


router = APIRouter(
    prefix="/api/admin",
    tags=["Administration"],
)


@router.get("/profile")
def admin_profile(
    current_user: AdminUser,
) -> dict[str, str | int]:
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role.value,
    }