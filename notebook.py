from collections import UserList
from field import Field
import re

class InvalidTagError(Exception):
    pass

class InvalidNoteError(Exception):
    pass

class Tag(Field):
    def is_valid(self, value :str):
        #conditions are: a tag must be a str and it's length must be less than 10 symbols
        #I think, it makes sense that tags must be short
        if type(value) == str and len(value) <= 10:
            return True
        else:
            raise InvalidTagError

class NoteText(Field):
    def is_valid(self, value :str):
        #The only condition is that the tag must be a string. For now at least
        if type(value) == str:
            return True
        else:
            raise InvalidNoteError

class Note:
    def __init__(self, text :NoteText, tags :list[Tag] = None) -> None:
        self.text = text
        self.tags = []
        if tags:
            self.tags += tags
    
    @property
    def text(self):
        return self.__text
    
    @text.setter
    def text(self, text):
        if type(text) == NoteText:
            self.__text = text

class Notebook(UserList):
    def notes_search_content(self, query):
        matching_notes = []
        if self.data:
            for note in self.data:
                if re.search(query, note.text.value, re.IGNORECASE):
                    matching_notes.append(note)
        return matching_notes

