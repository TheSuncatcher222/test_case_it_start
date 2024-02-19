from uuid import UUID

from fastapi import Depends, HTTPException, Security, status
from fastapi_jwt import JwtAuthorizationCredentials
from jose import JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.user_crud import crud_user
from src.database.database import get_async_session
from src.models.user import User
from src.schemas.jwt_token import TokenPayload
from src.security.jwt_token import access_security


async def get_current_user(
    credentials: JwtAuthorizationCredentials = Security(access_security),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    if credentials is None:
        raise HTTPException(
            detail='Ошибка авторизации.',
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    try:
        token_user = TokenPayload(**credentials.subject)
    except (JWTError, ValidationError):
        raise HTTPException(
            detail='Ошибка авторизации.',
            status_code=status.HTTP_403_FORBIDDEN,
        )
    return await get_user(session=session, user_uid=token_user.uid)


async def get_user(
    session: AsyncSession,
    user_uid: UUID,
) -> User:
    user = await crud_user.retrieve_by_uid(session=session, uid=user_uid)
    if not user:
        raise HTTPException(
            detail='Пользователь не найден.',
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return user
