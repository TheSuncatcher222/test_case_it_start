from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.api.dependencies.auth import get_current_user
from src.crud.device_crud import device_crud
from src.database.database import get_async_session
from src.models.device import Device
from src.models.user import User
from src.schemas.device import DeviceRepresentSchema, DeviceCreateSchema, DevicePreCreateSchema

router = APIRouter()


@router.post(
    path='/',
    response_model=DeviceRepresentSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_device(
    create_data: DevicePreCreateSchema,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Эндпоинт регистрации нового устройства."""

    serial: str = create_data.serial

    query = select(Device).where(Device.serial == serial)
    res = await session.execute(query)
    res = res.scalars().first()
    if res is not None:
        return HTTPException(
            detail=f'Устройство с серийным номером "{serial}" уже зарегистрировано.',
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    create_data = DeviceCreateSchema(user_id=current_user.id, **create_data.model_dump())

    return await device_crud.create(session=session, obj_data=create_data)


@router.get(
    path='/',
    response_model=list[DeviceRepresentSchema],
    status_code=status.HTTP_200_OK,
)
async def retrieve_devices(
    session: AsyncSession = Depends(get_async_session),
    limit: int = 100,
    offset: int = 0,
):
    return await device_crud.retrieve_multi(session=session, limit=limit, offset=offset)
