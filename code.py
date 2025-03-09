import random # Для генерации весов
import numpy as np
import pandas as pd  # Для удобства работы с таблицами

# Реализация алгоритма first fit 
def first_fit(items, bin_capacity):
    bins = []
    for item in items:
        placed = False
        for i, bin_ in enumerate(bins):
            if sum(bin_) + item <= bin_capacity:
                bins[i].append(item)
                placed = True
                break
        if not placed:
            bins.append([item])
    return bins

def calculate_fragmentation(bins, bin_capacity):
    total_free_space = sum(bin_capacity - sum(bin_) for bin_ in bins)
    total_space = len(bins) * bin_capacity
    return total_free_space / total_space

def calculate_max_weight_ratio(items, bin_capacity):
    return max(items) / bin_capacity

def calculate_fill_rate(bins, bin_capacity):
    total_filled_space = sum(sum(bin_) for bin_ in bins)
    total_space = len(bins) * bin_capacity
    return total_filled_space / total_space

# Уровни факторов
fragmentation_levels = [0.2, 0.5, 0.8]
max_weight_ratio_levels = [0.1, 0.5, 0.9]
num_items_levels = [50, 100, 150]
fill_rate_levels = [0.3, 0.5, 0.7]

# Вместимость контейнера (можно изменить)
bin_capacity = 1.0

# Список для хранения результатов
results = []
num_of_experiments = 5

epsilon = 0.2
# Проведение экспериментов

for frag in fragmentation_levels:
    for weight_ratio in max_weight_ratio_levels:
        for num_items in num_items_levels:
            for fill in fill_rate_levels:
                all_results = []
                for i in range(num_of_experiments):
                    # Генерация случайных предметов
                    items = [random.uniform(0.1, weight_ratio) for _ in range(num_items)]
                    #while True:
                    # Запуск алгоритма First Fit
                    bins = first_fit(items, bin_capacity)
                    # Расчет коэффициентов
                    fragmentation = calculate_fragmentation(bins, bin_capacity)
                    max_weight_ratio = calculate_max_weight_ratio(items, bin_capacity)
                    fill_rate = calculate_fill_rate(bins, bin_capacity)
                    #if abs(fragmentations - frag) > epsilon or
                    
                    all_results.append(len(bins))
                    # Добавление результатов в список
                result_row = []
                result_row.append(frag)
                result_row.append(weight_ratio)
                result_row.append(num_items)
                for elem in all_results:
                    result_row.append(elem)
                #results.append([frag, weight_ratio, num_items, fill, len(bins), fragmentation, max_weight_ratio, fill_rate])
                results.append(result_row)

# Создание DataFrame и сохранение в CSV
# Этот DataFrame создавался для просмотра разницы между фактическими и целевыми значениями
df = pd.DataFrame(results, columns=['X_1', 'X_2', 'X_3', 'X_4', 'Y1', 'Y2', 'Y3', 'Y4'])

#df_for_excel = df[['X_1', 'X_2', 'X_3', 'X_4', 'Y1']]

# df['X_1 (fact)'] = pd.to_numeric(df['X_1 (fact)'])
# df['X_2 (fact)'] = pd.to_numeric(df['X_2 (fact)'])
# df['X_4 (fact)'] = pd.to_numeric(df['X_4 (fact)'])
df.to_excel("results.xlsx", index=False)

print("Результаты сохранены в файл results.xlsx")