from datetime import date
from typing import Optional

from pydantic import BaseModel


class DeviceDataBaseSchema(BaseModel):
    data_x: float
    data_y: float
    data_z: float


class DeviceDataPreCreateSchema(DeviceDataBaseSchema):
    pass


class DeviceDataCreateSchema(DeviceDataPreCreateSchema):
    device_id: int


class DeviceDataUpdateSchema(DeviceDataCreateSchema):
    pass


class FromDate(BaseModel):
    from_date: Optional[date] = None
