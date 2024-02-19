from calendar import timegm
from datetime import datetime, timedelta, timezone
from typing import Optional, TypedDict

from fastapi_jwt import JwtAccessBearerCookie, JwtRefreshBearer
from jose import JWSError, jwt

from src.config.config import settings
from src.schemas.jwt_token import TokenAccessRefresh, TokenPayload

access_security = JwtAccessBearerCookie(
    secret_key=settings.JWT_SECRET_KEY,
    auto_error=True,
    access_expires_delta=timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRES_MIN),
)

refresh_security = JwtRefreshBearer(
    secret_key=settings.JWT_SECRET_KEY,
    refresh_expires_delta=timedelta(
        minutes=settings.JWT_REFRESH_TOKEN_EXPIRES_MIN
    ),
    auto_error=True,
)


class TokenSubject(TypedDict):
    uid: str


async def create_tokens(subject: TokenSubject) -> TokenAccessRefresh:
    access_token = await create_access_token(subject)
    refresh_token = await create_refresh_token(subject)
    return TokenAccessRefresh(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


async def create_access_token(subject: TokenSubject) -> str:
    return access_security.create_access_token(subject=subject)


async def create_refresh_token(subject: TokenSubject) -> str:
    return refresh_security.create_refresh_token(
        subject=subject,
        expires_delta=timedelta(minutes=settings.JWT_REFRESH_TOKEN_EXPIRES_MIN),
    )


async def extract_token_payload(
    token: str, secret_key: str, algorithm: str, check_expired: bool = False
) -> Optional[TokenPayload]:
    try:
        payload = jwt.decode(token, secret_key, algorithm)
    except JWSError:
        return None

    if check_expired:
        exp = payload["exp"]

        now = timegm(datetime.now(timezone.utc).utctimetuple())
        if now > exp:
            return None

    return TokenPayload(**payload["subject"])
