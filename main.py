from pathlib import Path

def parse_input(user_input):
    tokens = user_input.split()
    command = tokens[0].lower()  # перший елемент - команда
    args = tokens[1:]  # решта елементів - аргументи
    return command, args

contacts = {}

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            print(f"Input error: {e}")
    return wrapper

@input_error
def add_contact(name, phone_number):
    contacts[name] = phone_number
    print("Contact added.")

@input_error
def change_contact(name, new_phone_number):
    if name in contacts:
        contacts[name] = new_phone_number
        print("Contact updated.")
    else:
        print("Contact not found.")

@input_error
def show_phone(name):
    if name in contacts:
        print(contacts[name])
    else:
        print("Contact not found.")

@input_error
def show_all():
    for name, phone_number in contacts.items():
        print(f"{name}: {phone_number}")

def main():
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command == "add":
            add_contact(*args)
        elif command == "change":
            change_contact(*args)
        elif command == "phone":
            show_phone(*args)
        elif command == "all":
            show_all()
        elif command == "close" or command == "exit":
            print("Good bye!")
            break
        else:
            print("Invalid command. Try again.")

if __name__ == "__main__":
    main()
from datetime import datetime, timedelta
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {', '.join(str(p) for p in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def search_by_name(self, name):
        return self.data.get(name)

    def delete_record(self, name):
        del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.now()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                if (record.birthday.value.month, record.birthday.value.day) in [(next_week.month, day) for day in range(next_week.day - 6, next_week.day + 1)]:
                    upcoming_birthdays.append(record)

        return upcoming_birthdays

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

def parse_input(user_input):
    tokens = user_input.split()
    command = tokens[0].lower()  # перший елемент - команда
    args = tokens[1:]  # решта елементів - аргументи
    return command, args

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            print(f"Input error: {e}")
    return wrapper

@input_error
def add_contact(book, name, phone_number):
    record = Record(name)
    record.add_phone(phone_number)
    book.add_record(record)
    print("Contact added.")

@input_error
def change_contact(book, name, new_phone_number):
    record = book.search_by_name(name)
    if record:
        record.add_phone(new_phone_number)
        print("Contact updated.")
    else:
        print("Contact not found.")

@input_error
def show_phone(book, name):
    record = book.search_by_name(name)
    if record:
        print(record.phones)
    else:
        print("Contact not found.")

@input_error
def show_all(book):
    print(book)

@input_error
def add_birthday(book, name, birthday):
    record = book.search_by_name(name)
    if record:
        record.add_birthday(birthday)
        print("Birthday added to the contact.")
    else:
        print("Contact not found.")

@input_error
def show_birthday(book, name):
    record = book.search_by_name(name)
    if record:
        if record.birthday:
            print(f"{record.name.value}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}")
        else:
            print("Birthday not set for this contact.")
    else:
        print("Contact not found.")

@input_error
def birthdays(book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        print("Upcoming birthdays:")
        for record in upcoming_birthdays:
            print(f"{record.name.value}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}")
    else:
        print("No upcoming birthdays in the next week.")

def main():
    book = AddressBook()
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command == "add":
            add_contact(book, *args)
        elif command == "change":
            change_contact(book, *args)
        elif command == "phone":
            show_phone(book, *args)
        elif command == "all":
            show_all(book)
        elif command == "add-birthday":
            add_birthday(book, *args)
        elif command == "show-birthday":
            show_birthday(book, *args)
        elif command == "birthdays":
            birthdays(book)
        elif command in ["close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command. Try again.")

if __name__ == "__main__":
    main()
