from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Boolean , DateTime , Enum as SqlEnum , String , func
from sqlalchemy.orm import Mapped , mapped_column , relationship 

from app.database.base import Base

if TYPE_CHECKING:
    from app.database.models.sale import Sale


class UserRole(str,Enum):
    ADMIN = "admin"
    CASHIER ="cashier"


class User(Base):
    __tablename__="users"
    id: Mapped[int] = mapped_column(primary_key=True)

    username:Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable= False
    )
    
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole, name="user_role"),
        default=UserRole.CASHIER,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    sales: Mapped[list["Sale"]] = relationship(
        back_populates="cashier",
    )