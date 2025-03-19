import rgr_functions

if __name__ == '__main__':
    num_items_list = [50, 100, 150]
    distribution_code_list = [1, 2, 3]  # Нормальное, равномерное, экспоненциальное
    large_items_ratio_list = [0.3, 0.4, 0.5]
    standard_ratio_list = [0.2, 0.5, 0.8]
    backpack_capacity = 200

    # Запуск эксперимента
    results = rgr_functions.run_experiment(num_items_list, distribution_code_list, large_items_ratio_list, standard_ratio_list, backpack_capacity)

    # Сохранение результатов в Excel
    rgr_functions.save_to_excel(results)