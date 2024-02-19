from datetime import date, datetime
import json

from sqlalchemy.sql import join, select

from src.celery.celery import celery_app
from src.database.database import sync_session_maker
from src.models.device import Device
from src.models.device_data import DeviceData
# INFO. Нужно, чтобы сессия нашла связь Device и User.
from src.models.user import User  # noqa (F401)
from src.utils.device_data.get_statistics import get_analyses


@celery_app.task(name='src.celery.device_data.tasks.get_data_analysis')
def get_data_analysis(user_id: int, from_date: date | None = None):
    """
    Производит анализа данных моделей DeviceData для указанного пользователя.

    Если указано from_date - фильтрует данные не старше указанного срока.

    Сохраняет результаты в текстовый файл.
    """
    with sync_session_maker() as session:
        joined_tables = join(DeviceData, Device, DeviceData.device_id == Device.id)

        if from_date is None:
            query = select(
                DeviceData
            ).select_from(
                joined_tables
            ).where(
                Device.user_id == user_id
            )
        else:
            query = select(
                DeviceData
            ).select_from(
                joined_tables
            ).where(
                Device.user_id == user_id,
                DeviceData.registered_at >= from_date
            )

        result = session.execute(query)
        device_data_objects = result.scalars().all()

    if not device_data_objects:
        analysis: dict[str, str] = {
            'items_count': 0,
            'min_x': 0,
            'min_y': 0,
            'min_z': 0,
            'max_x': 0,
            'max_y': 0,
            'max_z': 0,
            'sum_x': 0,
            'sum_y': 0,
            'sum_z': 0,
        }

    else:
        device_data_list = [None] * len(device_data_objects)
        i: int = 0
        for obj in device_data_objects:
            device_data_list[i] = {
                'data_x': obj.data_x,
                'data_y': obj.data_y,
                'data_z': obj.data_z,
            }
            i += 1
        analysis: dict[str, str] = get_analyses(device_data_list=device_data_list)

    datetime_now: str = datetime.utcnow()
    formatted_datetime = datetime_now.strftime('%Y-%m-%d_%H-%M-%S')
    report_name: str = f'src/reports/{user_id}__{formatted_datetime}.json'
    with open(report_name, 'w') as file:
        json.dump(analysis, file)

    return
