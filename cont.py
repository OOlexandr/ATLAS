import csv

# Создаем пустой словарь, который будет служить в качестве справочника контактов
contacts = {}

# Основной цикл программы
while True:
    print("Выберите действие:")
    print("1 - Добавить контакт")
    print("2 - Найти контакт")
    print("3 - Удалить контакт")
    print("4 - Вывести все контакты")
    print("5 - Экспортировать контакты в файл CSV")
    print("6 - Выйти")

    # Запрашиваем у пользователя действие
    choice = input("Введите номер действия: ")

    # Добавление контакта
    if choice == "1":
        name = input("Введите имя контакта: ")
        phone = input("Введите номер телефона: ")
        email = input("Введите адрес электронной почты: ")
        contacts[name] = {"phone": phone, "email": email}
        print("Контакт успешно добавлен.")

    # Поиск контакта
    elif choice == "2":
        name = input("Введите имя контакта: ")
        if name in contacts:
            print(f"Номер телефона: {contacts[name]['phone']}")
            print(f"Адрес электронной почты: {contacts[name]['email']}")
        else:
            print("Контакт не найден.")

    # Удаление контакта
    elif choice == "3":
        name = input("Введите имя контакта: ")
        if name in contacts:
            del contacts[name]
            print("Контакт успешно удален.")
        else:
            print("Контакт не найден.")

    # Вывод всех контактов
    elif choice == "4":
        if contacts:
            for name, info in contacts.items():
                print(name)
                print(f"Номер телефона: {info['phone']}")
                print(f"Адрес электронной почты: {info['email']}")
        else:
            print("Список контактов пуст.")

    # Экспортирование контактов в файл CSV
    elif choice == "5":
        if contacts:
            # Записываем данные в файл CSV
            with open("contacts.csv", "w", newline="") as csvfile:
                fieldnames = ["Name", "Phone", "Email"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for name, info in contacts.items():
                    writer.writerow({"Name": name, "Phone": info["phone"], "Email": info["email"]})

            print("Контакты успешно экспортированы в файл contacts.csv.")
        else:
            print("Список контактов пуст.")

    # Выход из программы
    elif choice == "6":
        break

    # Некорректный ввод
    else:
        print("Некорректный ввод. Пожалуйста, повторите попытку.")