from src.crud.base_crud import BaseAsyncCrud
from src.models.device_data import DeviceData
from src.schemas.device_data import DeviceDataCreateSchema, DeviceDataUpdateSchema


class DeviceDataCrud(BaseAsyncCrud[DeviceData, DeviceDataCreateSchema, DeviceDataUpdateSchema]):
    pass


device_data_crud = DeviceDataCrud(DeviceData)
