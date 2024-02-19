import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies.auth import get_current_user
from src.crud.device_crud import device_crud
from src.crud.user_crud import crud_user
from src.database.database import get_async_session
from src.models.user import User
from src.schemas.user import UserCreate, UserPreCreate, UserResponse
from src.security.password import hash_password

router = APIRouter()


@router.post(
    path='/',
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    create_data: UserPreCreate,
    session: AsyncSession = Depends(get_async_session),
):
    user = await crud_user.retrieve_by_email(session=session, email=create_data.email)
    if user:
        raise HTTPException(
            detail=(
                'Пользователь с указанным адресом '
                'электронной почты уже существует.',
            ),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    create_data = create_data.model_dump(exclude_unset=True)
    hashed_password = await hash_password(create_data.pop("password"))
    random_uid = str(uuid.uuid4())

    return await crud_user.create(
        session=session,
        obj_data=UserCreate(
            uid=random_uid,
            hashed_password=hashed_password,
            **create_data,
        ),
    )


@router.get(
    path='/my-devices',
    status_code=status.HTTP_200_OK,
)
async def retrieve_user_devices(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    user = await crud_user.retrieve_by_uid(session=session, uid=current_user.uid)
    if not user:
        raise HTTPException(
            detail='Пользователь не найден.',
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return await device_crud.retrieve_by_user_id(session=session, user_id=user.id)
