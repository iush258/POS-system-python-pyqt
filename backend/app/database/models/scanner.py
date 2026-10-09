from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.database.models.user import User


class ScannerSession(Base):
    __tablename__ = "scanner_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)

    session_token: Mapped[UUID] = mapped_column(
        default=uuid4,
        unique=True,
        index=True,
        nullable=False,
    )

    pos_session_id: Mapped[str] = mapped_column(
        String(255),
        index=True,
        nullable=False,
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )

    is_cashier_present: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    creator: Mapped["User"] = relationship()