from collections import UserList
from field import Field
import re
import pickle
import copy


class InvalidTagError(Exception):
    pass


class InvalidNoteError(Exception):
    pass


class InvalidNameError(Exception):
    pass


class Name(Field):
    def is_valid(self, value):
        if type(value) == str: 
            return True
        else:
            raise InvalidNameError


class Tag(Field):
    def is_valid(self, value: str):
        # conditions are: a tag must be a str and it's length must be less than 10 symbols
        # I think, it makes sense that tags must be short
        if type(value) == str and len(value) <= 10:
            return True
        else:
            raise InvalidTagError


class NoteText(Field):
    def is_valid(self, value: str):
        # The only condition is that the tag must be a string. For now at least
        if type(value) == str:
            return True
        else:
            raise InvalidNoteError


class Note:
    def __init__(self, name: Name, text: NoteText, tags: list[Tag] = None) -> None:
        self.name = name
        self.text = text

        #  Гиевский 02052023 - переделал если параметр tag заходит то tags так и останется списком
        self.tags = [tags] if tags else []
        # self.tags = []
        #  Гиевский 02052023 - Закоментировал, так как дабовление в список происходит через .append
        # if tags:
        #     self.tags += tags
    
    # Gievskiy 02052023
    def add_note_tag(self, tag:Tag):
        self.tags.append(tag)

    def __str__(self) -> str:
        return f'Note : {self.name}, {self.text}, {self.tags}'
    
    def __repr__(self) -> str:
        return f'Note : {self.name}, {self.text}, {self.tags}'

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        if type(text) == NoteText:
            self.__text = text


class Notebook(UserList):
    def __init__(self):
        super().__init__()
        self.file_name = 'notes_12_team.bin'

    def __str__(self) -> str:
        return super().__str__()
    
    def __repr__(self) -> str:
        return super().__repr__()
        
    def notes_search_content(self, query):
        matching_notes = []
        if self.data:
            for note in self.data:
                if re.search(query, note.text.value, re.IGNORECASE):
                    matching_notes.append(note)
        return matching_notes
        
    def save_notes_to_file(self):
        with open(self.file_name, 'wb') as fh:
            pickle.dump(self, fh)

    def load_notes_from_file(self):
        try:
            with open(self.file_name, 'rb') as fh:
                notes = pickle.load(fh)
                if notes:
                    self.data = copy.deepcopy(notes.data)
        except:
            pass
            
    def delete_note(self, note_name: str):
        if note_name:
            for note in self.data:
                if note.name.value == note_name:
                    self.data.remove(note)
                    return True
        return False

    def get_data_list(self):
        names_list = []
        for note in self.data:
            names_list.append(note.name.value)
        return names_list
