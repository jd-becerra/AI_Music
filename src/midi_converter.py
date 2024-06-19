import collections
import pandas as pd
import numpy as np
import pretty_midi

def midi_to_notes(midi_file: str) -> pd.DataFrame:
    try:
        pm = pretty_midi.PrettyMIDI(midi_file)
        print(pm)
        for instrument in pm.instruments:
            if not instrument.is_drum:
                print(instrument)
                notes = collections.defaultdict(list)

                # Sort the notes by start time
                sorted_notes = sorted(instrument.notes, key=lambda note: note.start)
                prev_start = sorted_notes[0].start

                for note in sorted_notes:
                    if note.start - prev_start > 0:
                        start = note.start
                        end = note.end
                        notes['pitch'].append(note.pitch)
                        notes['start'].append(start)
                        notes['end'].append(end)
                        notes['step'].append(start - prev_start)
                        notes['duration'].append(end - start)
                        notes['velocity'].append(note.velocity)
                        prev_start = start
                return pd.DataFrame({name: np.array(value) for name, value in notes.items()})
    except Exception as e:
        print(f'Error processing {midi_file}: {e}')


def notes_to_midi(
            notes: pd.DataFrame,
            out_file: str, 
            instrument_name: str,
            velocity: int = 100,  # note loudness
        ) -> pretty_midi.PrettyMIDI:

    pm = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(
        program=pretty_midi.instrument_name_to_program(
            instrument_name))

    prev_start = 0
    for i, note in notes.iterrows():
        start = float(prev_start + note['step'])
        end = float(start + note['duration'])
        note = pretty_midi.Note(
            velocity=velocity,
            pitch=int(note['pitch']),
            start=start,
            end=end,
        )
        instrument.notes.append(note)
        prev_start = start

    pm.instruments.append(instrument)
    pm.write(out_file)
    return pm
