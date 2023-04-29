import pickle

file_name = 'notes_12_team.bin'

def save_notes_to_file(file_name, notes):
    with open(file_name, 'wb') as fh:
        pickle.dump(notes, fh)

def load_notes_from_file(file_name):
    with open(file_name, 'rb') as fh:
        notes = pickle.load(fh)
        return notes

print(save_notes_to_file('notes_12_team.bin', {123 , 'call', 'Manual'}))

print(load_notes_from_file('notes_12_team.bin'))