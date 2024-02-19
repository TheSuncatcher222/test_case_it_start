from re import fullmatch

from pydantic import BaseModel, validator

DEVICE_SERIAL_REGEX: str = r'^[a-zA-Z0-9]{6}$'
DEVICE_SERIAL_ERR: str = (
    'Укажите валидный серийный номер устройства, состоящий из'
    'шести (6) символов (буквы A-Z и цифры 0-9)'
)


class DevicePreCreateSchema(BaseModel):
    serial: str

    @validator('serial')
    def validate_serial(value: str) -> str:
        """
        Производит валидацию серийного номера устройства.
        Заменяет строчные буквы заглавными.
        """
        if fullmatch(pattern=DEVICE_SERIAL_REGEX, string=value) is None:
            raise ValueError(DEVICE_SERIAL_ERR)
        return value.upper()


class DeviceCreateSchema(DevicePreCreateSchema):
    user_id: int


class DeviceRepresentSchema(BaseModel):
    id: int
    serial: str


class DeviceUpdateSchema(DevicePreCreateSchema):
    pass
