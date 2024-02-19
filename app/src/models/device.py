from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.database import Base

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.device_data import DeviceData


class Device(Base):
    __tablename__ = 'table_device'

    id: Mapped[int] = mapped_column(
        comment='id устройства',
        index=True,
        primary_key=True,
    )
    serial: Mapped[str] = mapped_column(
        String,
        comment='Серийный номер устройства',
        unique=True,
    )

    user: Mapped['User'] = relationship(
        'User',
        back_populates='device',
        single_parent=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            'table_user.id',
            ondelete='CASCADE',
        ),
        comment='Пользователь устройства',
    )
    data: Mapped['DeviceData'] = relationship(
        'DeviceData',
        back_populates='device',
        single_parent=True,
    )
