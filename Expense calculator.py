all_expenses = [["еда", 5500], ["напитки", 4000], ["одежда", 10000]]

while True:
    category = input("Введите категорию расхода (или 'стоп' для завершения): ")
    if category.lower() == "стоп":
        break

    amount_input = input(f'Введите сумму расхода для категории "{category}": ')
    try:
        amount = float(amount_input)
        all_expenses.append([category, amount])
        print(f"Добавлено: {category} - {amount} руб.")
    except ValueError:
        print("Ошибка! Введите числовое значение для суммы!")

print("Список всех трат:", all_expenses)
total = sum(expense[1] for expense in all_expenses)
print(f"Общая сумма расходов: {total} руб.")