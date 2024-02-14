import csv
import os


# Файл для хранения данных справочника
DATA_FILE = 'phonebook.csv'
# Заголовки столбцов
HEADERS = ['Фамилия', 'Имя', 'Отчество', 'Организация', 'Рабочий телефон', 'Личный телефон']
# Размер страницы
global page_size
page_size= 5


def load_data() -> list:
    """Загрузка данных из файла."""
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def save_data(data: list):
    """Сохранение данных в файл."""
    with open(DATA_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(data)


def print_table(data: list):
    """Печать таблицы данных с красивым форматированием."""
    column_widths = {header: len(header) for header in HEADERS}
    for entry in data:
        for header in HEADERS:
            column_widths[header] = max(column_widths[header], len(entry.get(header, '')))

    header_row = ' | '.join(header.ljust(column_widths[header]) for header in HEADERS)
    print(header_row)
    print('-' * len(header_row))

    for entry in data:
        row = ' | '.join(entry.get(header, '').ljust(column_widths[header]) for header in HEADERS)
        print(row)


def add_entry():
    """Добавление новой записи в справочник."""
    new_entry = {header: input(f'{header}: ') for header in HEADERS}
    data = load_data()
    data.append(new_entry)
    save_data(data)
    print("Запись добавлена.")


def search_entries_for_edit_delete() -> list:
    """Поиск записей для последующего редактирования или удаления."""
    print("Введите критерии поиска. Оставьте поле пустым, если хотите пропустить его.")
    search_criteria = {header: input(f'{header}: ').lower() for header in HEADERS}
    data = load_data()
    found_entries = [entry for entry in data if all(entry.get(header, '').lower().startswith(search_criteria[header]) for header in HEADERS if search_criteria[header])]
    if found_entries:
        print_table(found_entries)
        return found_entries
    else:
        print("Записи не найдены.")
        return []


def select_entry_from_list(found_entries: list) -> int:
    """Выбор записи из списка найденных."""
    try:
        entry_number = int(input("Выберите номер записи: ")) - 1
        if 0 <= entry_number < len(found_entries):
            return entry_number
        else:
            print("Некорректный номер записи.")
            return None
    except ValueError:
        print("Некорректный ввод. Пожалуйста, введите число.")
        return None


def edit_entry():
    """Редактирование записи в справочнике по нескольким критериям."""
    found_entries = search_entries_for_edit_delete()
    if found_entries:
        entry_number = select_entry_from_list(found_entries)
        if entry_number is not None:
            data = load_data()
            entry_to_edit = found_entries[entry_number]
            updated_entry = {}
            for header in HEADERS:
                try:
                    new_value = input(f'{header} [{entry_to_edit[header]}]: ')
                    if new_value.strip():  # Проверяем, ввел ли пользователь новое значение
                        updated_entry[header] = new_value.strip()
                    else:
                        updated_entry[header] = entry_to_edit[header]  # Сохраняем прежнее значение, если пользователь не ввел новое
                except Exception as e:
                    print(f"Ошибка ввода: {e}")
            # Обновляем запись в списке данных
            data[data.index(entry_to_edit)] = updated_entry
            save_data(data)
            print("Запись обновлена.")


def delete_entry():
    """Удаление записи из справочника по нескольким критериям."""
    found_entries = search_entries_for_edit_delete()
    if found_entries:
        entry_number = select_entry_from_list(found_entries)
        if entry_number is not None:
            data = load_data()
            # Удаляем запись из списка данных
            data.remove(found_entries[entry_number])
            save_data(data)
            print("Запись удалена.")


def search_entries():
    """Поиск записей по одной или нескольким характеристикам."""
    print("Введите критерии поиска. Оставьте поле пустым, если хотите пропустить его.")
    search_criteria = {header: input(f'{header}: ').lower() for header in HEADERS}
    data = load_data()
    found_entries = [entry for entry in data if all(entry.get(header, '').lower().startswith(search_criteria[header]) for header in HEADERS if search_criteria[header])]
    if found_entries:
        print_table(found_entries)
    else:
        print("Записи не найдены.")


def display_entries():
    """Вывод записей постранично."""
    data = load_data()
    global page_size
    pages = len(data) // page_size + (1 if len(data) % page_size > 0 else 0)
    for page in range(pages):
        print(f"\nСтраница {page + 1}/{pages}")
        start_index = page * page_size
        end_index = start_index + page_size
        print_table(data[start_index:end_index])
        input("Нажмите Enter для продолжения...")


def change_page_size():
    """Изменение размера страницы."""
    try:
        global page_size
        new_page_size = int(input("Введите новый размер страницы: "))
        if new_page_size <= 0:
            print("Размер страницы должен быть положительным числом.")
            return
        page_size = new_page_size
    except ValueError:
        print("Некорректный ввод. Размер страницы остается прежним.")


def main():
    """Основная функция программы."""
    actions = {'1': display_entries, '2': add_entry, '3': edit_entry, '4': search_entries, '5': delete_entry, '6': change_page_size}
    while True:
        print("\nТелефонный справочник")
        print("1. Вывести записи")
        print("2. Добавить запись")
        print("3. Редактировать запись")
        print("4. Поиск записей")
        print("5. Удалить запись")
        print("6. Изменить размер страницы")
        print("0. Выход")
        choice = input("Выберите действие: ")
        if choice == '0':
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Некорректный выбор. Попробуйте снова.")



if __name__ == "__main__":
    main()
