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
def get_pitch_distribution_from_song_dict(song_dict):
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

def get_pitch_from_song_dict(song_dict):
    pitch_list = song_dict['cpitch']
    pitch_list = np.array(pitch_list)
    return pitch_list

def get_duration_from_song_dict(song_dict):
    duration_list = song_dict['dur']
    duration_list = np.array(duration_list)
    return duration_list

def get_melody_name_from_song_dict(song_dict):
    melody_name = song_dict['melody.name'][0]
    melody_name = np.array(melody_name, dtype=str)
    return melody_name

## overall probability, information.content and entropy:===========================================

def get_overall_prob_from_song_dict(song_dict):
    overall_prob = song_dict['probability']
    overall_prob = np.array(overall_prob)
    return overall_prob

def get_overall_information_content_from_song_dict(song_dict):
    overall_ic = song_dict['information.content']
    overall_ic = np.array(overall_ic)
    return overall_ic

def get_overall_entropy_from_song_dict(song_dict):
    overall_entropy = song_dict['entropy']
    overall_entropy = np.array(overall_entropy)
    return overall_entropy

#=========================================================================


## melodic expectation features:================================================================

def get_cpitch_information_content_from_song_dict(song_dict):
    # returns 2 columns: "pitch MIDI number" and the correspondent "cpitch.information.content"
    cpitch_ic = song_dict['cpitch.information.content']
    cpitch_ic = np.array(cpitch_ic)
    pitch = get_pitch_from_song_dict(song_dict)
    cpitch_information_content = np.column_stack((pitch, cpitch_ic))
    return cpitch_information_content

def get_cpitch_entropy_from_song_dict(song_dict):
    cpitch_entro = song_dict['cpitch.entropy']
    cpitch_entro = np.array(cpitch_entro)
    pitch = get_pitch_from_song_dict(song_dict)
    cpitch_entropy = np.column_stack((pitch, cpitch_entro))
    return cpitch_entropy

def get_onset_information_content_from_song_dict(song_dict):
    onset_ic = song_dict['onset.information.content']
    onset_ic = np.array(onset_ic)
    onset = get_onset_from_song_dict(song_dict)
    onset_information_content = np.column_stack((onset, onset_ic))
    return onset_information_content

def get_onset_entropy_from_song_dict(song_dict):
    onset_entro = song_dict['onset.entropy']
    onset_entro = np.array(onset_entro)
    onset = get_onset_from_song_dict(song_dict)
    onset_entropy = np.column_stack((onset, onset_entro))
    return onset_entropy

def get_duration_information_content_from_song_dict(song_dict):
    duration_ic = song_dict['dur.information.content']
    duration_ic = np.array(duration_ic)
    duration = get_duration_from_song_dict(song_dict)
    duration_information_content = np.column_stack((duration, duration_ic))
    return duration_information_content

def get_duration_entropy_from_song_dict(song_dict):
    duration_entro = song_dict['dur.entropy']
    duration_entro = np.array(duration_entro)
    duration = get_duration_from_song_dict(song_dict)
    duration_entropy = np.column_stack((duration, duration_entro))
    return duration_entropy
#=========================================================================




def get_aligned_surprise_with_onset_from_song_dict(song_dict):
    surprise = get_surprise_from_song_dict(song_dict)
    onset = get_onset_from_song_dict(song_dict)
    aligned_surprise_with_onset = np.column_stack((onset, surprise))
    return aligned_surprise_with_onset

def get_aligned_pitch_with_duration_from_song_dict(song_dict):
    pitch = get_pitch_from_song_dict(song_dict)
    duration = get_duration_from_song_dict(song_dict)
    aligned_pitch_with_duration = np.column_stack((duration, pitch))
    return aligned_pitch_with_duration

def get_aligned_pitch_with_onset_from_song_dict(song_dict):
    pitch = get_pitch_from_song_dict(song_dict)
    onset = get_onset_from_song_dict(song_dict)
    aligned_pitch_with_onset = np.column_stack((onset, pitch))
    return aligned_pitch_with_onset

def get_aligned_surprise_with_pitch_from_song_dict(song_dict):
    surprise = get_surprise_from_song_dict(song_dict)
    pitch = get_pitch_from_song_dict(song_dict)
    aligned_surprise_with_pitch = np.column_stack((pitch, surprise))
    return aligned_surprise_with_pitch




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


