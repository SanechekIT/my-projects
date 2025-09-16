def universal_calculator(operation, *args, **kwargs):
    """
    Args:
        operation (str): операция ('+', '-', '*', '/', 'avg')
        *args: числа для вычислений
        **kwargs: дополнительные параметры:
            round_result (bool): округлять ли результат (по умолчанию False)
            decimal_places (int): количество знаков после запятой (по умолчанию 2)

    Returns:
        float или int: результат вычислений
    """
    # Получаем параметры из kwargs с значениями по умолчанию
    round_result = kwargs.get('round_result', False)
    decimal_places = kwargs.get('decimal_places', 2)

    # Проверяем, что переданы числа
    if not args:
        raise ValueError("Не переданы числа для вычислений")

    # Выполняем операцию
    if operation == '+':
        result = sum(args)
    elif operation == '-':
        result = args[0] - sum(args[1:])
    elif operation == '*':
        result = 1
        for num in args:
            result *= num
    elif operation == '/':
        if len(args) < 2:
            raise ValueError("Для деления нужно минимум 2 числа")
        result = args[0]
        for num in args[1:]:
            if num == 0:
                raise ZeroDivisionError("Деление на ноль")
            result /= num
    elif operation == 'avg':
        result = sum(args) / len(args)
    else:
        raise ValueError(f"Неподдерживаемая операция: {operation}")

    # Обрабатываем результат в соответствии с параметрами
    if round_result:
        result = round(result, decimal_places)
        # Если округлилось до целого, возвращаем int
        if result == int(result):
            return int(result)
        return result

    return result


# Примеры использования
if __name__ == "__main__":
    # Пример 1: Сложение с округлением
    print(universal_calculator('+', 1.234, 2.567, 3.891, round_result=True, decimal_places=2))
    # Вывод: 7.69

    # Пример 2: Среднее значение
    print(universal_calculator('avg', 10, 20, 30, 40, round_result=True))
    # Вывод: 25.0

    # Пример 3: Умножение без округления
    print(universal_calculator('*', 2.5, 3, 4.1))
    # Вывод: 30.75

    # Пример 4: Деление
    print(universal_calculator('/', 100, 3, 2, round_result=True, decimal_places=3))
    # Вывод: 16.667

    # Пример 5: Вычитание
    print(universal_calculator('-', 100, 20, 10, 5))
    # Вывод: 65