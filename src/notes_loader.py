import pickle
import pandas as pd
from midi_converter import midi_to_notes

def get_notes(files):
    all_notes = pd.DataFrame()
    for file in files:
        notes = midi_to_notes(file)
        print(f'Extracted notes from {file}')
        all_notes = pd.concat([all_notes, notes], axis=0)
    return all_notes

def save_notes_to_file(notes, savefile_name):
    with open(savefile_name, 'wb') as file:
        pickle.dump(notes, file)
    print(f'Saved {len(notes)} notes to {savefile_name}')

def load_notes_from_file(dump_file_path):
    with open(dump_file_path, "rb") as filepath:
        notes = pickle.load(filepath)
    print(f'Loaded {len(notes)} notes from {dump_file_path}')
    return notes
