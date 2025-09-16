import json
import os


class Phonebook:
    def __init__(self, filename='phonebook.json'):
        self.filename = filename
        self.contacts = self.load_contacts()

    def load_contacts(self):
        """Загрузка контактов из файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    return json.load(file)
            except:
                return {}
        return {}

    def save_contacts(self):
        """Сохранение контактов в файл"""
        with open(self.filename, 'w') as file:
            json.dump(self.contacts, file, indent=2)
        print("Контакты сохранены!")

    def add_contact(self):
        """Добавление нового контакта"""
        print("\n--- Добавить контакт ---")

        name = input("Имя: ").strip()
        if not name:
            print("Имя не может быть пустым!")
            return

        if name in self.contacts:
            print("Контакт уже существует!")
            return

        phone = input("Телефон: ").strip()
        email = input("Email: ").strip()

        self.contacts[name] = {
            'phone': phone,
            'email': email
        }

        print(f"Контакт '{name}' добавлен!")

    def find_contact(self):
        """Поиск контакта"""
        print("\n--- Поиск контакта ---")
        search = input("Имя или номер: ").lower()

        found = False
        for name, data in self.contacts.items():
            if search in name.lower() or search in data['phone']:
                print(f"\nИмя: {name}")
                print(f"Телефон: {data['phone']}")
                print(f"Email: {data['email']}")
                found = True

        if not found:
            print("Контакты не найдены!")

    def view_all(self):
        """Просмотр всех контактов"""
        print("\n--- Все контакты ---")

        if not self.contacts:
            print("Телефонная книга пуста!")
            return

        for name, data in self.contacts.items():
            print(f"\nИмя: {name}")
            print(f"Телефон: {data['phone']}")
            print(f"Email: {data['email']}")

    def edit_contact(self):
        """Редактирование контакта"""
        print("\n--- Редактировать контакт ---")
        name = input("Имя контакта: ")

        if name not in self.contacts:
            print("Контакт не найден!")
            return

        print("Новые данные (оставьте пустым чтобы не менять):")
        new_phone = input("Новый телефон: ")
        new_email = input("Новый email: ")

        if new_phone:
            self.contacts[name]['phone'] = new_phone
        if new_email:
            self.contacts[name]['email'] = new_email

        print("Контакт обновлен!")

    def delete_contact(self):
        """Удаление контакта"""
        print("\n--- Удалить контакт ---")
        name = input("Имя контакта: ")

        if name not in self.contacts:
            print("Контакт не найден!")
            return

        confirm = input(f"Удалить '{name}'? (y/n): ")
        if confirm.lower() == 'y':
            del self.contacts[name]
            print("Контакт удален!")

    def run(self):
        """Основное меню"""
        while True:
            print("\n" + "=" * 30)
            print("ТЕЛЕФОННЫЙ СПРАВОЧНИК")
            print("=" * 30)
            print("1. Добавить контакт")
            print("2. Найти контакт")
            print("3. Все контакты")
            print("4. Редактировать")
            print("5. Удалить")
            print("6. Сохранить и выйти")
            print("7. Выйти без сохранения")

            choice = input("\nВыберите (1-7): ")

            if choice == '1':
                self.add_contact()
            elif choice == '2':
                self.find_contact()
            elif choice == '3':
                self.view_all()
            elif choice == '4':
                self.edit_contact()
            elif choice == '5':
                self.delete_contact()
            elif choice == '6':
                self.save_contacts()
                print("До свидания!")
                break
            elif choice == '7':
                print("Выход без сохранения")
                break
            else:
                print("Неверный выбор!")


# Запуск программы
if __name__ == "__main__":
    phonebook = Phonebook()
    phonebook.run()