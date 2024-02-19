import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.database.database import Base

if TYPE_CHECKING:
    from src.models.device import Device


class User(Base):
    __tablename__ = 'table_user'

    id: Mapped[int] = mapped_column(
        comment='id пользователя',
        index=True,
        primary_key=True,
    )
    uid: Mapped[uuid.UUID] = mapped_column(
        UUID,
        comment='uuid пользователя',
        default=uuid.uuid4,
        index=True,
        unique=True,
    )
    first_name: Mapped[str] = mapped_column(
        comment='имя пользователя',
    )
    second_name: Mapped[str] = mapped_column(
        comment='фамилия пользователя',
    )
    email: Mapped[str] = mapped_column(
        comment='email пользователя',
        index=True,
        unique=True,
    )
    hashed_password: Mapped[str] = mapped_column(
        comment='хеш пароля пользователя',
    )
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        comment='дата регистрации пользователя',
        server_default=func.now(),
        index=True,
    )

    device: Mapped['Device'] = relationship(
        'Device',
        back_populates='user',
    )

    @property
    def fullname(self) -> str:
        return f'{self.second_name} {self.first_name}'

    def __str__(self) -> str:
        return f'{self.id} - {self.fullname}'
