import numpy as np
import mido
from lisp import parser as lisp


"""
This module contains helper functions (pure functions) to extract {various data} from {various formats}
"""

my_pitch_range = (47,91)

# extract {python readable dictionary (a collection of song_dict)} from {.dat file}

def get_all_song_dict_from_dat(dat_file_path):
    all_song_dict = lisp.getDico(dat_file_path)
    return all_song_dict


# extract {data of interest} from {song_dict}
def get_note_distribution_from_song_dict(song_dict):
    pitch_distribution = []
    song_length = len(song_dict['cpitch.probability'])
    for i in range(*my_pitch_range):
        key_to_look = 'cpitch.' + str(i)
        if key_to_look not in song_dict.keys():
            one_pitch_prob_across_time = [0] * song_length
        else:
            one_pitch_prob_across_time = song_dict[key_to_look]
        pitch_distribution.append(one_pitch_prob_across_time)

    pitch_distribution = np.array(pitch_distribution).T
    return pitch_distribution

def get_onset_from_song_dict(song_dict):
    onset_list = song_dict['onset']
    onset_list = np.array(onset_list)
    return onset_list

def get_surprise_from_song_dict(song_dict):
    probability_seq = song_dict['probability']
    probability_seq = np.array(probability_seq)
    surprise = -np.log(probability_seq)/np.log(2)
    return surprise

def get_aligned_surprise_with_onset_from_song_dict(song_dict):
    surprise = get_surprise_from_song_dict(song_dict)
    onset = get_onset_from_song_dict(song_dict)
    aligned_surprise_with_onset = np.column_stack((onset, surprise))

    return aligned_surprise_with_onset

def get_melody_name_from_song_dict(song_dict):
    melody_name = song_dict['melody.name'][0]
    melody_name = np.array(melody_name, dtype=str)
    return melody_name


# extract {data of interest} from {midi}

def get_pitch_sequence_from_midi(midi_file_path):
    mymidi = mido.MidiFile(midi_file_path, type=0)
    track = mymidi.tracks[0]
    pitch_sequence = []
    for msg in track:
        if msg.type == 'note_on':
            pitch_sequence.append(msg.note)
    pitch_sequence = np.array(pitch_sequence)
    return pitch_sequence


