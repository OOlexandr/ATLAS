import address_book
import notebook
from move_main import main_sort, InvalidPath

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.completion import NestedCompleter

from config import use_promt_toolkit, pre_command_text

class NameNotGivenError(Exception):
    pass


class PhoneNotGivenError(Exception):
    pass


class BirthdayNotGivenError(Exception):
    pass


class PathNotGivenError(Exception):
    pass


class TextNotGivenError(Exception):
    pass

class NoteNameNotGivenError(Exception):
    pass

contacts = address_book.AddressBook()
notes = notebook.Notebook()


def error_handler(func):
    def inner(args):
        try:
            return func(args)
        except KeyError:
            return "The user is not in the address book"
        except address_book.InvalidPhoneError:
            return "Number is invalid"
        except address_book.InvalidNameError:
            return "Name is invalid"  # I don't expect ever getting it.
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
        except TextNotGivenError:
            return "Please enter text to find"
        except NoteNameNotGivenError:
            return "Please enter note name to delete"
    return inner


# handlers
# every handler acceptslist of arguments and returns message to be printed to command line
@error_handler
def handler_greetings(args):
    return "How can I help you?"


@error_handler
def handler_exit(args):
    return "Good bye!"


# Тут бачу можливість покращення. Зараз ця функція приймає аргументи виключно в порядку
# ім'я, номер, дата народження. Можливо можна зробити її більш гнучкою та зручною для користувача.
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
def find_note(args):
    if len(args) == 0:
        raise TextNotGivenError
    text = ' '.join(args)
    found_notes = notes.notes_search_content(text)
    if found_notes:
        message = "found notes are:\n"
        for n in found_notes:
            message += "\n" + n.text.value
        return message
    return "No notes found"


@error_handler
def delete_note(args):
    if len(args) == 0:
        raise NoteNameNotGivenError
    note_name = args[0]
    if notes.delete_note(note_name):
        return f"Note {note_name} successfully deleted"
    else:
        return f"Can't delete note: {note_name}!"


handlers = {"hello": {"func": handler_greetings, "help_message": "Just greeting!"},
            "good bye": {"func": handler_exit, "help_message": "exit from bot"},
            "close": {"func": handler_exit, "help_message": "exit from bot"},
            "exit": {"func": handler_exit, "help_message": "exit from bot"},
            "add record": {"func": handler_add, "help_message": "add record ContactName ContactPhone Contactbirthday"},
            "add birthday": {"func": handler_add_birthday, "help_message": "add birthday ContactName Contactbirthday"},
            "add phone": {"func": handler_add_phone, "help_message": "add phone ContactName ContactPhone"},
            "change": {"func": handler_change, "help_message": "change ContactName OldPhone NewPhone"},
            "phone": {"func": handler_phone, "help_message": "phone ContactName"},
            "days to birthday": {"func": handler_days_to_birthday, "help_message": "days to birthday ContactName"},
            "show all": {"func": handler_show_all, "help_message": "showed all contacts"},
            "find note": {"func": find_note, "help_message": "find NoteText"},
            "find": {"func": find, "help_message": "find ContactName"},
            "sort": {"func": sort, "help_message": "sort FolderPath"},
            "delnote": {"func": delete_note, "help_message": "delnote NoteName"}}


# key - command, value - handler.

# parcer
def parce(command):
    # returns list. first element - handler and the rest are arguments
    # returns None if command is not recognized
    command = command.strip().lower()
    parced_command = []
    for handler in handlers:
        if command.startswith(handler):
            command = command.removeprefix(handler)
            parced_command.append(handlers[handler]["func"])
            break
    if parced_command:
        parced_command += command.split()
        return parced_command
    return None


comands_list_meta_dict = {}
comands_nested_dict = {}

for k, v in handlers.items():

    comands_nested_dict.update({k:None})

    comands_list_meta_dict.update({k: v["help_message"]})

# def update_nested_dict()
#     global need_nested_dict_udate
#     if need_nested_dict_udate:
#
#
#
#         need_nested_dict_udate = False




def main():
    if use_promt_toolkit:
        session = PromptSession()
        contacts.read_contacts()
        notes.load_notes_from_file()

    while True:

        if use_promt_toolkit:
            input_text = session.prompt(pre_command_text, auto_suggest=AutoSuggestFromHistory(),
                                        completer=NestedCompleter.from_nested_dict(comands_nested_dict))

            # input_text = session.prompt(pre_command_text, auto_suggest=AutoSuggestFromHistory(),
            #                   completer=WordCompleter(comands_list, meta_dict=comands_list_meta_dict, sentence=True))
        else:
            input_text = input(pre_command_text)

        command = parce(input_text)
        if command:
            result = command[0](command[1:])
            print(result)
            if result == "Good bye!":
                contacts.save_contacts()
                notes.save_notes_to_file()
                return
        else:
            print("unknown command")


if __name__ == '__main__':
    main()
