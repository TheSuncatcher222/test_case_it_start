from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.database.database import Base

if TYPE_CHECKING:
    from src.models.device import Device


class DeviceData(Base):
    __tablename__ = 'table_device_data'

    id: Mapped[int] = mapped_column(
        comment='id записи',
        index=True,
        primary_key=True,
    )
    # INFO. Лучше использовать decimal из typing.
    data_x: Mapped[float] = mapped_column(
        comment='Данные "x"'
    )
    data_y: Mapped[float] = mapped_column(
        comment='Данные "y"'
    )
    data_z: Mapped[float] = mapped_column(
        comment='Данные "z"'
    )
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        comment='дата регистрации пользователя',
        server_default=func.now(),
        index=True,
    )

    device: Mapped['Device'] = relationship(
        'Device',
        back_populates='data',
        single_parent=True,
    )
    device_id: Mapped[int] = mapped_column(
        ForeignKey(
            'table_device.id',
            ondelete='CASCADE',
        ),
        comment='Устройство',
    )
