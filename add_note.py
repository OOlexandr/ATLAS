import datetime


class Note:
    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        self.status = 'not done'


class Notes:
    def __init__(self):
        self.notes_list = []

    def add(self, title, text):
        note = Note(title, text)
        self.notes_list.append(note)
        return f'"{note.title}" has been added to your Notes'

    def __str__(self):
        if self.notes_list:
            notes_str = ""
            for i, note in enumerate(self.notes_list, start=1):
                notes_str += f"{i}. {note}\n"
            return notes_str
        else:
            return 'You have no notes.'


class NotesApp:
    def __init__(self):
        self.notes = Notes()

    def input_error(func):
        def wrapper(*args):
            try:
                return func(*args)
            except ValueError:
                return 'Please enter a valid command.'
            except IndexError:
                return 'Please enter a note.'

        return wrapper

    @input_error
    def add_note(self, *args):
        title, text = args
        return self.notes.add(title, text)

    COMMANDS = {'addnote': add_note}

    def command_handler(self, text):
        for command, function in self.COMMANDS.items():
            if text.lower().startswith(command):
                data = text[len(command):].strip()
                return function, data.split(' ', 1)
        return None, ''

    def main(self):
        while True:
            user_input = input('>>> ')
            command, data = self.command_handler(user_input)
            if not command:
                print("Unknown command, try again.")
                continue
            print(command(self, *data))
            if command == exit:
                break


if __name__ == '__main__':
    app = NotesApp()
    app.main()
