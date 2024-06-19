from notes_loader import load_notes_from_file
from glob import glob
import random

notes_file = '../data/small_sample'
notes = load_notes_from_file(notes_file)
print(notes)

# NEXT: create model
