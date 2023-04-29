"""Пошук нотаток за змістом нотатки"""


import re

def notes_search_content(notes, query):
    matching_notes = []
    for note in notes:
        if re.search(query, note, re.IGNORECASE):
            matching_notes.append(note)
    return matching_notes

print (notes_search_content({'first note', 'second', 'Third note', 'third car', 'fourth note'}, 'third'))