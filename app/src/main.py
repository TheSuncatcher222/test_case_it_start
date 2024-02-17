"""
Главный модуль FastAPI сервиса.

Осуществляет запуск проекта, подключение базы данных, регистрацию эндпоинтов.
"""

import os
import sys

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn

# INFO: добавляет корневую директорию проекта в sys.path для возможности
#       использования абсолютных путей импорта данных из модулей.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api.router import router as api_router
from src.config.config import settings
from src.config.logger import Logger, get_logger

app: FastAPI = FastAPI(
    debug=settings.DEBUG,
    title='IT Start',
    description='Test case for Gazprom Neft',
    version='0.0.1',
    openapi_url='/api/docs/openapi.json',
    docs_url='/api/docs/swagger',
    redoc_url='/api/docs/redoc',
)

logger: Logger = get_logger(name=__name__)

allowed_origins = [
    'http://localhost:80',
    f'https://{settings.DOMAIN_IP}',
    f'https://{settings.DOMAIN_NAME}',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    router=api_router,
    prefix='/api',
)

if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=settings.ASGI_PORT,
        reload=True,
        workers=settings.WORKERS_AMOUNT,
    )
