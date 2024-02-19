import statistics


def get_analyses(device_data_list: list[dict[str, float]]):
    """Производит анализа числовых характеристик."""
    items_count = len(device_data_list)

    data_x, data_y, data_z = separate_data(device_data_list=device_data_list)

    min_x: float = get_min_value(data_x)
    min_y: float = get_min_value(data_y)
    min_z: float = get_min_value(data_z)

    max_x: float = get_max_value(data_x)
    max_y: float = get_max_value(data_y)
    max_z: float = get_max_value(data_z)

    sum_x: float = get_sum_value(data_x)
    sum_y: float = get_sum_value(data_y)
    sum_z: float = get_sum_value(data_z)

    return {
        'items_count': items_count,
        'min_x': min_x,
        'min_y': min_y,
        'min_z': min_z,
        'max_x': max_x,
        'max_y': max_y,
        'max_z': max_z,
        'sum_x': sum_x,
        'sum_y': sum_y,
        'sum_z': sum_z,
    }


def separate_data(device_data_list: list[dict[str, float]]) -> tuple[list[float]]:
    """Извлекает и разделяет из данных устройств показания для x, y, z."""
    data_x: list[float] = [None] * len(device_data_list)
    data_y: list[float] = [None] * len(device_data_list)
    data_z: list[float] = [None] * len(device_data_list)
    i: int = 0
    for data in device_data_list:
        data_x[i]: float = data['data_x']
        data_y[i]: float = data['data_y']
        data_z[i]: float = data['data_z']
        i += 1
    return data_x, data_y, data_z


def get_min_value(data: list[float]) -> float:
    """Находит минимальное значение в списке чисел."""
    return min(data)


def get_max_value(data: list[float]) -> float:
    """Находит максимальное значение в списке чисел."""
    return max(data)


def get_sum_value(data: list[float]) -> float:
    """Находит сумму значений в списке чисел."""
    return sum(data)


def get_median(data: list[float]) -> float:
    return statistics.median(data)
