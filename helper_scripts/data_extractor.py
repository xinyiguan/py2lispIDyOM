import numpy as np
import mido
from lisp import parser as lisp

"""
This module contains helper functions (pure functions) to extract {various data} from {various formats}
"""

# extract {python readable dictionary (a collection of song_dict)} from {.dat file}

def get_all_song_dict_from_dat(dat_file_path):
    all_song_dict = lisp.getDico(dat_file_path)
    return all_song_dict

def get_song_dict_of_interest(all_song_dict, melody_id):
    return list(all_song_dict.values())[melody_id]


# extractors of database identifiers from song dict:  ==================================================================
"""
This set of functions is used for extracting the database identifiers.
With this Python interface, dataset id's are different from those in the original IDyOM: 
    - train dataset are initialized by "66" and followed by the timestamp of each experiment trial.
    - test dataset are initialized by "99" and followed by the timestamp of each experiment trial.
"""


def get_melody_name_from_song_dict(song_dict):
    melody_name = song_dict['melody.name'][0]
    melody_name = np.array(melody_name, dtype=str)
    return melody_name


# extractors of musical properties of the event from song_dict: ========================================================
""""
This mainly corresponds to the basic viewpoints
"""
def get_onset_from_song_dict(song_dict):
    onset_list = song_dict['onset']
    onset_list = np.array(onset_list)
    return onset_list

def get_pitch_from_song_dict(song_dict):
    pitch_list = song_dict['cpitch']
    pitch_list = np.array(pitch_list)
    return pitch_list

def get_duration_from_song_dict(song_dict):
    duration_list = song_dict['dur']
    duration_list = np.array(duration_list)
    return duration_list

def get_keysig_from_song_dict(song_dict):
    keysig_list = song_dict['keysig']
    keysig_list = np.array(keysig_list)
    return keysig_list

def get_mode_from_song_dict(song_dict):
    mode_list = song_dict['mode']
    mode_list = np.array(mode_list)
    return mode_list

def get_tempo_from_song_dict(song_dict):
    tempo_list = song_dict['tempo']
    tempo_list = np.array(tempo_list)
    return tempo_list

def get_pulses_from_song_dict(song_dict):
    pulses_list = song_dict['pulses']
    pulses_list = np.array(pulses_list)
    return pulses_list

def get_barlength_from_song_dict(song_dict):
    barlength_list = song_dict['barlength']
    barlength_list = np.array(barlength_list)
    return barlength_list

def get_deltast_from_song_dict(song_dict):
    deltast_list = song_dict['deltast']
    deltast_list = np.array(deltast_list)
    return deltast_list

def get_bioi_from_song_dict(song_dict):
    bioi_list = song_dict['bioi']
    bioi_list = np.array(bioi_list)
    return bioi_list

def get_phrase_from_song_dict(song_dict):
    phrase_list = song_dict['phrase']
    phrase_list = np.array(phrase_list)
    return phrase_list

# Additional Viewpoints
def get_mpitch_from_song_dict(song_dict):
    mpitch_list = song_dict['mpitch']
    mpitch_list = np.array(mpitch_list)
    return mpitch_list

def get_accidental_from_song_dict(song_dict):
    accidental_list = song_dict['accidental']
    accidental_list = np.array(accidental_list)
    return accidental_list

def get_dyn_from_song_dict(song_dict):
    dyn_list = song_dict['dyn']
    dyn_list = np.array(dyn_list)
    return dyn_list

def get_voice_from_song_dict(song_dict):
    voice_list = song_dict['voice']
    voice_list = np.array(voice_list)
    return voice_list

def get_ornament_from_song_dict(song_dict):
    ornament_list = song_dict['ornament']
    ornament_list = np.array(ornament_list)
    return ornament_list

def get_comma_from_song_dict(song_dict):
    comma_list = song_dict['comma']
    comma_list = np.array(comma_list)
    return comma_list

def get_articulation_from_song_dict(song_dict):
    articulation_list = song_dict['articulation']
    articulation_list = np.array(articulation_list)
    return articulation_list


# extractors of model outputs from song_dict: ========================================================
"""
...

"""
## overall probability, information.content and entropy:

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


##  probability, information content and entropy estimated by the model for each target viewpoint:
"""
This set of functions will return 2 colums:
    1st column: value for the target viewpoint
    2nd column: corresponding probability/information content/entropy value for the target viewpoint
    
Current version supports target viewpoint of cpitch and onset 
"""
### melodic expectation features:

def get_cpitch_probabililty_from_song_dict(song_dict):
    # returns 2 columns: "pitch MIDI number" and the correspondent "cpitch.probability"
    cpitch_prob = song_dict['cpitch.probability']
    cpitch_prob = np.array(cpitch_prob)
    pitch = get_pitch_from_song_dict(song_dict)
    cpitch_probability = np.column_stack((pitch, cpitch_prob))
    return cpitch_probability

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

def get_onset_probability_content_from_song_dict(song_dict):
    onset_prob = song_dict['onset.probability']
    onset_prob = np.array(onset_prob)
    onset = get_onset_from_song_dict(song_dict)
    onset_probability = np.column_stack((onset, onset_prob))
    return onset_probability

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

def get_duration_probability_content_from_song_dict(song_dict):
    duration_prob = song_dict['duration.probability']
    duration_prob = np.array(duration_prob)
    duration = get_duration_from_song_dict(song_dict)
    duration_probability = np.column_stack((duration, duration_prob))
    return duration_probability

def get_duration_information_content_from_song_dict(song_dict):
    duration_ic = song_dict['duration.information.content']
    duration_ic = np.array(duration_ic)
    duration = get_duration_from_song_dict(song_dict)
    duration_information_content = np.column_stack((duration, duration_ic))
    return duration_information_content

def get_duration_entropy_from_song_dict(song_dict):
    duration_entro = song_dict['duration.entropy']
    duration_entro = np.array(duration_entro)
    duration = get_duration_from_song_dict(song_dict)
    duration_entropy = np.column_stack((duration, duration_entro))
    return duration_entropy


# extract {data of interest} from {song_dict}
my_pitch_range = (47,91)


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


