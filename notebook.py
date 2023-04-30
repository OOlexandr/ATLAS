from collections import UserList
from field import Field

class InvalidTagError(Exception):
    pass

class InvalidNoteError(Exception):
    pass

class Title(Field): #Gievskiy 
    pass

class Tag(Field):
    # Gievskiy 30042023
    def __init__(self, value=None):
        self.value = value
    
    @property
    def value(self):
        return self._value
        
    @value.setter
    def value(self, value):
        if value is None:
            self._value = value
        else:
            self._value = self.is_valid(value)
    # **** 30042023
    
    # def is_valid(self, value: str):
    def is_valid(self, tag: str):
        # conditions are: a tag must be a str and it's length must be less than 10 symbols
        # I think, it makes sense that tags must be short
        
        if not type(tag) == str:
            raise ValueError
        elif len(tag) > 10:
            raise InvalidTagError
        return tag
        
        # if type(value) == str and len(value) <= 10:
        #     return True
        # else:
        #     raise InvalidTagError

class NoteText(Field):
    def is_valid(self, value :str):
        #The only condition is that the tag must be a string. For now at least
        if type(value) == str:
            return True
        else:
            raise InvalidNoteError

class Note:
    # Gevskiy 30042023 
    def __init__(self, text: NoteText, tag:Tag = None) -> None:
        self.text = text
        self.tags = [tag] if tag else []
    
    # def __init__(self, text: NoteText, tags: list[Tag] = None) -> None:
    #     self.text = text
    #     self.tags = []
    #     if tags:
    #         self.tags += tags
    #  **** 30042023
    
    def add_note_tag(self, tag:Tag):
        self.tags.append(tag)
    
    def change_note(self, old_text:NoteText, new_text:NoteText, old_tag:Tag, new_tag:Tag):
        for i, p in enumerate(self.title):
            if p.value == old_text.value:
                self.title[i] = new_text
                return f'Phone {old_text} change to {new_text}'
            
            if p.value == old_tag.value:
                self.title[i] = new_tag
                return f'Phone {old_tag} change to {new_tag}'
        return f'{old_text} - {new_text}, {old_tag} - {new_tag}'  
    #  **** 30042023
        
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

    def add_note(self, text: NoteText, *tags: Tag) -> Note:
        note = Note(text, tags)
        self.data.append(note)
        return note

#  Gievskiy 300420223
#  functions
# Decorator input errors
notebook = Notebook ()

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            raise KeyError
        except ValueError:
            raise ValueError
        except IndexError:
            raise IndexError
        except TypeError:
            raise TypeError
    return wrapper

# Add an entry with a tag
@input_error
def add_note_tag(*args, **kwargs):
    title = Title(args[0])
    text = NoteText(args[1])
    tag = Tag(args[2])
        
    rec = notebook.get(title.value)
    if not rec:
        rec: Note = Note(title,  text, tag)
        notebook.add_note(rec)
    
    rec.add_note_tag(tag)
    return f"{title} : {text}, {tag} has been added to the NoteBook"

# text change
@input_error
def note_change(*args, **kwargs):
    title = Title(args[0])
    old_text = NoteText(args[1])
    new_text = NoteText(args[2])
    old_tag = NoteText(args[3])
    new_tag = NoteText(args[4])
    
    rec = notebook.get(title.value)
    
    if rec:
        return rec.change_note(old_text, new_text, old_tag, new_tag)
    
    return f'NoteBook has no contact {title}'
# *** 30042023

