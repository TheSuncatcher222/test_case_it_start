from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base_crud import BaseAsyncCrud, ModelType
from src.models.device import Device
from src.schemas.device import DeviceCreateSchema, DeviceUpdateSchema


class DeviceCrud(BaseAsyncCrud[Device, DeviceCreateSchema, DeviceUpdateSchema]):

    async def retrieve_by_user_id(
        self,
        *,
        session: AsyncSession,
        user_id: int,
    ) -> list[ModelType]:
        """Возвращает объект с указанным uuid из базы данных."""
        statement = select(self.model).where(self.model.user_id == user_id)
        result = await session.execute(statement)
        return result.scalars().all()


device_crud = DeviceCrud(Device)
