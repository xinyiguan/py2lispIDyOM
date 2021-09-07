"""
This script is to reconstruct midi files from the viewpoints extracted in IDyOM, using midiutil.

viewpoints used for reconstruction: pitch, duration, onset, tempo
"""

import midiutil
import os
from helper_scripts import data_extractor as data_extractor
from glob import glob



def miditempo2bpm(tempo):
    # 1 minute is 60 million microseconds.
    return (60 * 1000000) / tempo
def miditemp_list2bpm_list(tempo_list):
    return [miditempo2bpm(tempo) for tempo in tempo_list]

def compose_midi_from_sequences(pitch_seq,onset_seq,tempo_seq, dur_seq):
    # initial midi file setting
    track = 0
    channel = 0
    time = 0  # in beats
    tempo = miditemp_list2bpm_list(tempo_seq)[0]  # beats per minute
    volume = 100  # from 0-127
    midi_file = midiutil.MIDIFile(1, adjust_origin=True)
    midi_file.addTempo(track, time, tempo)

    # add notes to midifile
    for i in range(len(pitch_seq)):
        pitch = int(pitch_seq[i])
        time = onset_seq[i]/24  # the time at which the note sounds, correspond to the onset (idyom uses basic time units, quarter note =24)
        duration = dur_seq[i]/24    # midiutil: 1 beat (quarter note) = 1
        midi_file.addNote(track=track, channel=channel, pitch=pitch, time=time, duration=duration, volume=volume)

    return midi_file

def save_midi(midi_file, file_name, output_path):
    filename = file_name
    with open(output_path+filename, 'wb') as output_file:
        midi_file.writeFile(output_file)
        print('midi file saved as ',file_name)


def compose_single_midi_from_song_dict(song_dict):
    melody_name = str(data_extractor.get_melody_name_from_song_dict(song_dict)).replace('"', '')
    pitch_seq = data_extractor.get_pitch_from_song_dict(song_dict)
    onset_seq = data_extractor.get_onset_from_song_dict(song_dict)
    dur_seq = data_extractor.get_duration_from_song_dict(song_dict)
    tempo_seq = data_extractor.get_tempo_from_song_dict(song_dict)

    single_midi = compose_midi_from_sequences(pitch_seq,onset_seq,tempo_seq, dur_seq)
    return single_midi, melody_name

def compose_batch_midi_from_all_song_dict(selected_experiment_history_folder):
    dat_file_path = sorted(glob(selected_experiment_history_folder + 'experiment_output_data_folder/*'))[0]
    all_song_dict = data_extractor.get_all_song_dict_from_dat(dat_file_path)
    num_of_songs_in_dict = len(all_song_dict.keys())
    output_folder = selected_experiment_history_folder + 'reconstructed_midi_files/'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(num_of_songs_in_dict):
        song_dict = data_extractor.get_song_dict_of_interest(all_song_dict,i)
        reconstructed_midi_file = compose_single_midi_from_song_dict(song_dict)[0]
        reconstruct_midi_name = 'reconstruct_' + compose_single_midi_from_song_dict(song_dict)[1]+'.mid'
        save_midi(midi_file=reconstructed_midi_file, file_name=reconstruct_midi_name, output_path=output_folder)


if __name__ == '__main__':
    selected_experiment_history_folder = '/Users/xinyiguan/Desktop/Codes/IDyOM_Python_Interface/experiment_history/03-08-21_13.40.14/'
    compose_batch_midi_from_all_song_dict(selected_experiment_history_folder)