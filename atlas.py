import address_book
import notebook
from move_main import main_sort, InvalidPath



class NameNotGivenError(Exception):
    pass

class PhoneNotGivenError(Exception):
    pass

class BirthdayNotGivenError(Exception):
    pass

class PathNotGivenError(Exception):
    pass

# кожен може зробити опис  команди
print ("""Hello, I'm a personal assistant. 
    You can use next commands:
        "hello": handler_greetings,
        "good bye": handler_exit,
        "close": handler_exit,
        "exit": handler_exit,
        "add record": handler_add,
        "add birthday": handler_add_birthday,
        "add phone": handler_add_phone,
        "change": handler_change,
        "phone": handler_phone,
        "days to birthday": handler_days_to_birthday,
        "show all": handler_show_all,
        "find": find,
        "sort": To sort the files, input the "sort" command and the path to the directory with the files by a space
        "help": To get help about the operation of the program, input the command help""")    


contacts = address_book.AddressBook()

def error_handler(func):
    def inner(args):
        try:
            return func(args)
        except KeyError:
            return "The user is not in the address book"
        except address_book.InvalidPhoneError:
            return "Number is invalid"
        except address_book.InvalidNameError:
            return "Name is invalid" #I don't expect ever getting it.
        except address_book.InvalidDateError:
            return "Birthday is invalid"
        except NameNotGivenError:
            return "Please enter user name"
        except PhoneNotGivenError:
            return "Please enter user name and number"
        except BirthdayNotGivenError:
            return "Please enter user name and birthday"
        except address_book.RecordAlreadyExists:
            return "The user is already in the address book"
        except address_book.PhoneAlreadyExistsError:
            return "The phone already exists"
        except address_book.PhoneNotFoundError:
            return "The phone is not found"
        except PathNotGivenError:
            return "Please enter path to the folder"
        except InvalidPath:
            return "The path is invalid"
    return inner

#handlers
#every handler acceptslist of arguments and returns message to be printed to command line
@error_handler
def handler_greetings(args):
    return "How can I help you?"

@error_handler
def handler_exit(args):
    return "Good bye!"

#Тут бачу можливість покращення. Зараз ця функція приймає аргументи виключно в порядку
#ім'я, номер, дата народження. Можливо можна зробити її більш гнучкою та зручною для користувача.
@error_handler
def handler_add(args):
    if len(args) < 1:
        raise NameNotGivenError
    name = address_book.Name(args[0])
    phone = address_book.Phone(args[1]) if args[1:] else None
    birthday = address_book.Birthday(args[2]) if args[2:] else None
    contacts.add_record(name, phone, birthday)
    return "Contact was added succesfully"

@error_handler
def handler_change(args):
    if len(args) < 3:
        raise PhoneNotGivenError
    old_phone = address_book.Phone(args[1])
    new_phone = address_book.Phone(args[2])
    contacts[args[0]].change_phone(old_phone, new_phone)
    return "Contact was changed succesfully"

@error_handler
def handler_add_birthday(args):
    if len(args) < 2:
        raise BirthdayNotGivenError
    birthday = address_book.Birthday(args[1])
    contacts[args[0]].birthday = birthday
    return "Birthday was added succesfully"

@error_handler
def handler_add_phone(args):
    if len(args) < 2:
        raise PhoneNotGivenError
    phone = address_book.Phone(args[1])
    contacts[args[0]].add_phone(phone)
    return "Phone was added succesfully"

@error_handler
def handler_phone(args):
    if len(args) < 1:
        raise NameNotGivenError
    contact = contacts[args[0]]
    result = contact.name.value + ':'
    for phone in contact.phones:
        result += " " + phone.value
    return result

@error_handler
def handler_days_to_birthday(args):
    if len(args) < 1:
        raise NameNotGivenError
    contact = contacts[args[0]]
    days = contact.days_to_birthday()
    if days:
        return f"There are {days} days until birthday"
    else:
        return "Contact's birthday is unknown"

@error_handler
def handler_show_all(args):
    if not contacts:
        return "Contacts list is currently empty"
    message = "Here are all saved contacts:"
    i = 1
    for c_list in contacts:
        message += f"\nPage {i}:"
        i += 1
        for c in c_list:
            c_str = "\n" + c.name.value + ':'
            for phone in c.phones:
                c_str += " " + phone.value
            message += c_str

    return message

@error_handler
def find(args):
    records = contacts.find_records(args[0])
    if records:
        message = "Found contacts are:"
        for r in records:
            c_str = "\n" + r.name.value + ':'
            for phone in r.phones:
                c_str += " " + phone.value
            message += c_str
        return message
    else:
        return "No contacts were found"

@error_handler
def sort(args):
    if len(args) == 0:
        raise PathNotGivenError
    main_sort(args[0])
    return "Files sorted succesfully"

@error_handler
def reference(args):
    return """Hello, I'm a bot. I will help you use the program.
        - For add contact to directory input <<< add 'name' 'phone number in format '+xx-xxx-xxx-xx-xx', 'email', 'Birthdate' in format dd-mm-yyyy'  >>> use a space without a comma
        - For find contact in directory input <<< find 'name'  >>> use a space without a comma
        - For search contact by name letters, input <<< search name letters
        - For show all contacts in directory input <<< show >>> 
        - For update contact in directory input <<< update 'name' 'new number'  >>> use a space without a comma
        - For return the number of days until the next birthday, enter <<<dtb "name">>>.
        - To exit the program input <<<exit>>> or <<<bye>>>
        - To sort the files, input the "sort" command and the path to the directory with the files by a space
        - To get help about the operation of the program, input the command help"""
        
        

handlers = {"hello": handler_greetings,
            "good bye": handler_exit,
            "close": handler_exit,
            "exit": handler_exit,
            "add record": handler_add,
            "add birthday": handler_add_birthday,
            "add phone": handler_add_phone,
            "change": handler_change,
            "phone": handler_phone,
            "days to birthday": handler_days_to_birthday,
            "show all": handler_show_all,
            "find": find,
            "sort": sort,
            "help": reference}
#key - command, value - handler.

#parcer
def parce(command):
    #returns list. first element - handler and the rest are arguments
    #returns None if command is not recognized
    command = command.strip().lower()
    parced_command = []
    for handler in handlers:
        if command.startswith(handler):
            command = command.removeprefix(handler)
            parced_command.append(handlers[handler])
            break
    if parced_command:
        parced_command += command.split()
        return parced_command
    return None

def main():
    contacts.read_contacts()
    while True:
        command = parce(input())
        if command:
            result = command[0](command[1:])
            print(result)
            if result == "Good bye!":
                contacts.save_contacts()
                return
        else:
            print("unknown command")

if __name__ == '__main__':
    main()