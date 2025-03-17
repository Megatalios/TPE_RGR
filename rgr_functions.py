import numpy as np
import pandas as pd

def is_standard(weight):
    """Проверяет, является ли вес "стандартным" (делится на 5).

    Args:
        weight: Вес предмета.

    Returns:
        True, если вес "стандартный", False в противном случае.
    """
    return weight % 5 == 0


def convert_to_standard(weight):
    """Преобразует "нестандартный" вес в ближайший "стандартный" вес.

    Args:
        weight: "Нестандартный" вес предмета.

    Returns:
        Ближайший "стандартный" вес.
    """
    # Нижняя граница
    lower_standard = weight // 5 * 5
    # Верхняя граница
    upper_standard = lower_standard + 5
    if weight - lower_standard <= upper_standard - weight:
        return lower_standard
    else:
        return upper_standard
    

# Принцип работы функции генератора-корректора:
# 1. Сначала генерируется список чисел с заданной вариацией 
# 2. Затем этот список сдвигается вправо или влево (чтобы увеличить или уменьшить количество "крупных" элементов)
#    Данный шаг корректирует один фактор, не меняя другой (если прибавить к каждому числу константу, то вариация не меняется)
# 3. После этого корректируем долю "стандартных" элементов (смещаем их к ближайжим "стандартным" соседям)
#    Это меняет вариацию, однако она остается достаточно близкой к целевой
def generate_weights(num_items, coef_variation, large_items_ratio, standard_ratio, backpack_capacity):
    """Генерирует случайную последовательность весов предметов с заданными параметрами.

    Args:
        num_items: Количество предметов.
        coef_variation: Коэффициент вариации весов предметов.
        large_items_ratio: Доля "крупных" предметов (вес >= 0.6 * backpack_capacity).
        standard_ratio: Доля "стандартных" весов (делятся на 5).
        backpack_capacity: Вместимость рюкзака.
        
    Returns:
        - Список весов предметов.
        - Словарь с вычисленными показателями:
            - "num_items": Количество предметов.
            - "coef_variation": Коэффициент вариации.
            - "large_items_ratio": Фактическая доля "крупных" предметов.
            - "standard_ratio": Фактическая доля "стандартных" предметов.
    """
    # 1. Генерация последовательности с заданным коэффициентом вариации
    mean_value = backpack_capacity // 2
    weights = np.clip(np.random.normal(mean_value, coef_variation * mean_value, num_items), 1, backpack_capacity).astype(int)

    # 2. Корректировка доли крупных предметов
    large_threshold = 0.6 * backpack_capacity
    current_large_ratio = np.sum(weights >= large_threshold) / num_items


    if current_large_ratio < large_items_ratio:
        # Смещаем последовательность вправо
        shift_value = int((large_items_ratio - current_large_ratio) * num_items)
        weights += shift_value
        weights = np.clip(weights, 1, backpack_capacity)  # Ensure weights stay within bounds
    elif current_large_ratio > large_items_ratio:
        # Смещаем последовательность влево
        shift_value = int((current_large_ratio - large_items_ratio) * num_items)
        weights -= shift_value
        weights = np.clip(weights, 1, backpack_capacity)  # Ensure weights stay within bounds

    # 3. Корректировка доли стандартных элементов
    current_standard_ratio = np.sum(np.array([is_standard(w) for w in weights])) / num_items
    if current_standard_ratio < standard_ratio:
        # Увеличиваем количество стандартных элементов
        num_to_convert = int((standard_ratio - current_standard_ratio) * num_items)
        non_standard_indices = np.where(np.array([not is_standard(w) for w in weights]))[0]
        indices_to_convert = np.random.choice(non_standard_indices, min(num_to_convert, len(non_standard_indices)), replace=False)
        for i in indices_to_convert:
            weights[i] = convert_to_standard(weights[i])
    elif current_standard_ratio > standard_ratio:
        # Уменьшаем количество стандартных элементов
        num_to_convert = int((current_standard_ratio - standard_ratio) * num_items)
        standard_indices = np.where(np.array([is_standard(w) for w in weights]))[0]
        indices_to_convert = np.random.choice(standard_indices, min(num_to_convert, len(standard_indices)), replace=False)
        for i in indices_to_convert:
            weights[i] += 1  # Или weights[i] -= 1, случайный выбор, чтобы минимизировать влияние на вариацию

    # Вычисление фактических показателей
    actual_large_items_ratio = np.sum(weights >= large_threshold) / num_items
    actual_standard_ratio = np.sum(np.array([is_standard(w) for w in weights])) / num_items
    actual_coef_variation = np.std(weights) / np.mean(weights)

    metrics = {
        "num_items": num_items,
        "coef_variation": actual_coef_variation,
        "large_items_ratio": actual_large_items_ratio,
        "standard_ratio": actual_standard_ratio,
    }

    return weights, metrics


def first_fit(weights, capacity):
    """Решает рюкзачную задачу с заданными параметрами

    Args:
        weights: Список весов, которые необходимо распределить
        capacity: Вместимость рюкзака.
        
    Returns:
        Количество рюкзаков, которые необходимо для упаковки всех весов
    """
    bins = []
    for weight in weights:
        placed = False
        for i in range(len(bins)):
            if bins[i] + weight <= capacity:
                bins[i] += weight
                placed = True
                break
        if not placed:
            bins.append(weight)
    return len(bins)


def run_experiment(num_items_list, variation_coef_list, large_items_ratio_list, standard_ratio_list, backpack_capacity):
    """Проводит серию экспериментов для заданных значений, а затем возвращает итоговую таблицу

    Args:
        num_items_list: Список с количеством предметов.
        variation_coef_list: Список с коэффициентами вариации весов предметов.
        large_items_ratio_list: Список с долями "крупных" предметов (вес >= 0.6 * backpack_capacity).
        standard_ratio_list: Список с долями "стандартных" весов (делятся на 5).
        backpack_capacity: Вместимость рюкзака.
        
    Returns:
        - Список, в каждой строчке содержащий:
            Количество предметов, Коэффициент вариации, Доля крупных предметов, Доля стандартных предметов, Среднее значение при алгоритме FF за 100 прогонов
    """
    result_list = []
    for num_items in num_items_list:
        for variation_coef in variation_coef_list:
            for large_items_ratio in large_items_ratio_list:
                for standard_ratio in standard_ratio_list:
                    y_values = []
                    for i in range(100):
                        weights, _ = generate_weights(num_items, variation_coef, large_items_ratio, standard_ratio, backpack_capacity)
                        result = first_fit(weights, backpack_capacity)
                        y_values.append(result)
                    result_list.append([num_items, variation_coef, large_items_ratio, standard_ratio, sum(y_values)/len(y_values)])
    return result_list


def save_to_excel(result_list, filename="experiment_results.xlsx"):
    """Сохраняет результаты эксперимента в Excel файл.

    Args:
        result_list: Список результатов эксперимента.
        filename: Имя файла для сохранения.
    """
    df = pd.DataFrame(result_list, columns=["Количество предметом", "Коэффициент вариации", "Доля \"крупных\" предметов", "Доля \"стандартных\" предметов", "Количество рюкзаков"])
    df.to_excel(filename, index=False)
    print(f"Результаты сохранены в {filename}")