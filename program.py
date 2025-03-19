import rgr_functions

if __name__ == '__main__':

    # num_items = 100
    # coef_variation = 0.2
    # large_items_ratio = 0.3
    # standard_ratio = 0.4
    # backpack_capacity = 200
    # mean_value = 100

    # weights, metrics = rgr_functions.generate_weights(num_items, coef_variation, large_items_ratio, standard_ratio, backpack_capacity)
    # print("Веса:", weights)
    # print("Показатели:", metrics)

    # Предположим, у вас есть функция generate_weights и first_fit

    # Пример данных для эксперимента
    # num_items_list = [50, 100]
    # variation_coef_list = [0.1, 0.2]
    # large_items_ratio_list = [0.2, 0.4]
    # standard_ratio_list = [0.3, 0.5]
    # backpack_capacity = 200

    # # Запуск эксперимента
    # results = rgr_functions.run_experiment(num_items_list, variation_coef_list, large_items_ratio_list, standard_ratio_list, backpack_capacity)

    # # Сохранение результатов в Excel
    # rgr_functions.save_to_excel(results)

    # Пример данных для эксперимента
    num_items_list = [50, 100]
    distribution_code_list = [1, 2, 3]  # Нормальное, равномерное, экспоненциальное
    large_items_ratio_list = [0.2, 0.4]
    standard_ratio_list = [0.3, 0.5]
    backpack_capacity = 200

    # Запуск эксперимента
    results = rgr_functions.run_experiment(num_items_list, distribution_code_list, large_items_ratio_list, standard_ratio_list, backpack_capacity)

    # Сохранение результатов в Excel
    rgr_functions.save_to_excel(results)