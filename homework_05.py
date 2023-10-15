from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value


class Phone(Field):
    def __init__(self, phone):
        if self.validate_phone(phone):
            self.value = phone
        else:
            raise ValueError("Номер телефону недійсний.")

    @staticmethod
    def validate_phone(phone):
        if phone.isdigit() and len(phone) == 10:
            return True
        return False
    

class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        phone_obj = Phone(phone)  
        self.phones.append(phone_obj)

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        print("Такий номер телефону не знайдений.")

    def edit_name(self, new_name):
        self.name = Name(new_name)

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            phone_to_edit.value = new_phone
        else:
            raise ValueError("Такий номер телефону не знайдений.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    

class AddressBook(UserDict):
    def add_record(self, record):
        if record.name.value in self.data:
            raise ValueError("Запис з таким іменем вже існує.")
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            print(f"Запис з іменем {name} не знайдений.")


def main():
        address_book = AddressBook()

        instruction = """
        Вітаю! Я ваш бот-помічник. Ось, що я можу для вас зробити:

        1. Додавати контакти та номери телефонів. Для цього використовуйте команду 'add'. 

        2. Показувати вам список всіх контактів та їх номерів телефонів. 
        Для цього використовуйте команду 'show all'.

        3. Змінювати номер існуючого контакту. Використовуйте команду 'change'.

        4. Виводити номер телефону для зазначеного контакту. Використовуйте команду 'phone'.

        5. Для завершення роботи введіть, good bye, exit, close або вийти.

        Будь ласка, користуйтесь цими командами для взаємодії зі мною. 
        Я готовий допомогти вам у керуванні вашими контактами.
        """

        print(instruction)

        while True:
            user_input = input("Введіть команду: ").lower()

            if user_input in ('вийти', 'good bye', 'close', 'exit'):
                print("Good bye")
                break
            elif user_input == 'привіт' or user_input == 'hello':
                print("How can I help you?")
            elif user_input.startswith('add '):
                name, phone = user_input[4:].split()
                record = Record(name)
                record.add_phone(phone)
                address_book.add_record(record)
                print(f"Контакт {name} з номером {phone} доданий.")
            elif user_input.startswith('change '):
                name, new_phone = user_input[7:].split()
                if name in address_book.data:
                    record = address_book.data[name]
                    phone_obj = Phone(new_phone)
                    record.edit_phone(record.find_phone(new_phone), phone_obj)
                    print(f"Номер телефону для контакту {name} змінено на {new_phone}")
                else:
                    print(f"Контакт з ім'ям {name} не знайдений.")
            elif user_input.startswith('phone '):
                name = user_input[6:]
                if name in address_book.data:
                    record = address_book.data[name]
                    phone_list = [str(phone.value) for phone in record.phones]
                    print(f"Номер телефону для контакту {name}: {', '.join(phone_list)}")
                else:
                    print(f"Контакт з ім'ям {name} не знайдений.")
            elif user_input == 'show all':
                if not address_book.data:
                    print("Список контактів порожній.")
                else:
                    result = "Список всіх контактів та їх номерів телефонів:\n"
                    for name, record in address_book.data.items():
                        phone_list = [str(phone.value) for phone in record.phones]
                        result += f"{name}: {', '.join(phone_list)}\n"
                    print(result)
            else:
                print("Спробуйте ще раз.")

if __name__ == "__main__":
    main()