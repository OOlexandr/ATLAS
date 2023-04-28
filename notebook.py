from collections import UserList
from field import Field

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
    pass

try:
    tesTag = Tag("test")
    print(tesTag)
    tesTag2 = Tag("not long")
    print(tesTag2)
    text = NoteText("this is a tast note. Nothing wrong should be here")
    print(text)
    n1 = Note(text)
    n2 = Note(text, [tesTag, tesTag2])
except:
    print("found an error")