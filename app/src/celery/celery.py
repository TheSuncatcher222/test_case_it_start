from celery import Celery

from src.config.config import settings

redis_url: str = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}'

celery_backend: str = f'{redis_url}/0'
celery_broker: str = f'{redis_url}/1'

celery_app: Celery = Celery(
    __name__,
    backend=celery_backend,
    broker=celery_broker,
)

celery_app.autodiscover_tasks(
    [
        'src.celery.device_data',
    ],
)
