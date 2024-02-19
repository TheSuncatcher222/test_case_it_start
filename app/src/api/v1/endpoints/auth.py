from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from src.crud.user_crud import user_crud
from src.schemas.jwt_token import TokenAccessRefresh, UserLogin
from src.security.password import verify_password
from src.security.jwt_token import create_tokens, refresh_security

router = APIRouter()


@router.post(
    path='/login/',
    response_model=TokenAccessRefresh,
)
async def login(
    user_login: UserLogin,
    session: AsyncSession = Depends(get_async_session)
):
    user = await user_crud.retrieve_by_email(session=session, email=user_login.email)

    if not user:
        raise HTTPException(
            detail='Указаны неверные адрес электронной почти и/или пароль.',
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    password_verified = await verify_password(
        plain_password=user_login.password,
        hashed_password=user.hashed_password,
    )
    if not password_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Указаны неверные адрес электронной почти и/или пароль.',
        )

    return await create_tokens(subject={'uid': str(user.uid)})


@router.post(
    path='/refresh/',
    response_model=TokenAccessRefresh,
    status_code=status.HTTP_200_OK,
)
async def refresh(
    credentials: JwtAuthorizationCredentials = Security(refresh_security),
):
    return await create_tokens(credentials.subject)
