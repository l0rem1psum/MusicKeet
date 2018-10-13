import argparse
import tensorflow as tf
from absl import flags
import os
from os.path import isfile, join

def reset_flags():
    for name in list(flags.FLAGS):
        delattr(flags.FLAGS, name)


from melody_rnn import melody_rnn_generate, melody_rnn_config_flags
melody_rnn_generate_func = melody_rnn_generate.melody_rnn_generate
reset_flags()
from improv_rnn import improv_rnn_generate
improv_rnn_generate_func = improv_rnn_generate.improv_rnn_generate
reset_flags()
from drums_rnn import drums_rnn_generate
drums_rnn_generate_func = drums_rnn_generate.drums_rnn_generate
reset_flags()
from polyphony_rnn import polyphony_rnn_generate
polyphony_rnn_generate_func = polyphony_rnn_generate.polyphony_rnn_generate
reset_flags()


def generate_audio(chord_dict, instrument='melody'):
    path = './telegram_generated'
    note_type = chord_dict['on_off']
    note = chord_dict['note']
    velocity = chord_dict['velocity']

    primer = []

    for idx, note_type in enumerate(note_type):
        if note_type == 'note_on':
            primer.append(note[idx])
            primer.append(velocity[idx])
        else:
            primer.append(note[idx])
            primer.append(-1)
    primer = str(primer)

    if instrument == 'melody':
        print("Started running")
        melody_rnn_config_flags.set_flags()
        melody_rnn_generate.set_flags()
        melody_rnn_generate_func(primer=primer)
        reset_flags()

    full_path = next((join(path, f) for f in os.listdir(path) if isfile(join(path, f))), "")
    print(full_path)
    print(full_path.split('/')[-1])
    filename = full_path.split('\\')[-1].split('.')[0]
    print(filename)
    return full_path, filename


