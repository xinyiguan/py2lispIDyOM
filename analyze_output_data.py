from lisp import parser as lisp
import numpy as np
import matplotlib.pyplot as plt
import music21
import mido
import os
import data_extractor
from glob import glob
from mpl_toolkits.axes_grid1 import make_axes_locatable

# load data (default path is for the newest experiment history file)
newest_experiment_history_path = sorted(glob('experiment_history/*'))[-1]+'/' # sorted the order of the list
selected_experiment_history_path = newest_experiment_history_path
dat_file_path = sorted(glob(selected_experiment_history_path+'experiment_output_data_folder/*'))[0]
#f = open(dat_file_path,'r')


my_pitch_range = (47,91)
# do whatever you want

folder_name = 'train_shanx_test_shanx'


### demonstration on using data_extractor to extract data from .dat file path--------------------------

# all_song_dict is python readable .dat file (model output) for all testing dataset.
all_song_dict = data_extractor.get_all_song_dict_from_dat(dat_file_path)
song_dict_of_interest= list(all_song_dict.values())[0] # one of the testing song result info.
#print('song_dict_of_interest.keys: ', song_dict_of_interest.keys())

aligned_surprise_with_onset = data_extractor.get_aligned_surprise_with_onset_from_song_dict(song_dict_of_interest)
print('aligned_surprise_with_onset: ', aligned_surprise_with_onset)


assert False
note_distribution = data_extractor.get_note_distribution_from_song_dict(song_dict_of_interest)
onset_sequence = data_extractor.get_onset_from_song_dict(song_dict_of_interest)
my_surprise_sequence = data_extractor.get_surprise_from_song_dict(song_dict_of_interest)
original_surprise_sequence = list(lisp.getSurprise(dat_file_path).values())[0]
print('note_distribution.shape: ',note_distribution.shape)
print('note_distribution: ',note_distribution)
print('onset_sequence.shape: ',onset_sequence.shape)
print('onset_sequence: ',onset_sequence)
print('my_surprise_sequence: ',my_surprise_sequence)


### ---------------------------------





# data encoding helpers

def get_pitch_distribution_from_sequence(pitch_sequence):
    """
    one-hot encode {ground truth pitch sequence} to {pitch distribution sequence}
    """
    pitch_sequence = np.array(pitch_sequence).reshape(-1,1)
    f = lambda x,y:(x,y+1)
    options = np.arange(*f(*my_pitch_range))
    distribution = pitch_sequence == options
    return distribution

## plot helpers

def plot_pitch_distribution(ax,pitch_distribution,title):
    ax.set_xlabel('Time step')
    ax.set_ylabel('Pitch (midi number)')
    #ax.set_title('Pitch distribution across time for song '+ midifile[midifile.rfind("/"):] )
    ax.set_title(title)
    x_extent = [0, pitch_distribution.shape[0]]
    y_extent = list(my_pitch_range)
    ax.set_xticks(np.arange(*(x_extent+[1])),minor = True)
    ax.set_yticks(np.arange(*(y_extent+[1])),minor = True)
    ax.imshow(pitch_distribution.T, origin='lower', extent=[0, pitch_distribution.shape[0]] + list(my_pitch_range))
    return ax

def plot_surprise_across_time(ax,surprise_across_time,title=None):
    x_extent = [0, surprise_across_time.shape[0]]
    ax.set_xticks(np.arange(*(x_extent + [1])), minor=True)


    print('surprise_across_time.reshape(1,-1):  ' , surprise_across_time.reshape(1,-1))
    print('surprise_across_time.reshape(1,-1).shape:  ',surprise_across_time.reshape(1,-1).shape)
    ax.set_xlabel(title)

    ax.imshow(surprise_across_time.reshape(1,-1),cmap='Greys',interpolation='gaussian',origin='lower',extent=x_extent+[0,1])
    return ax





## the following is plot specfic song (ground truth and prediction accoriding to surprise)

def make_figure_from_index(index):
    S = list(lisp.getSurprise(dat_file_path).values())[index]
    S = np.array(S)
    D = data_extractor.get_all_song_dict_from_dat(dat_file_path)
    this_song_result = list(D.values())[index]
    song_dict = this_song_result

    midifile = sorted(glob(selected_experiment_history_path+'experiment_input_data_folder/test/'+'*'))[index]

    pitch_sequence = get_pitch_sequence_from_midi(midifile)
    pitch_distritbution = get_pitch_distribution_from_sequence(pitch_sequence)

    predicted_pitch_distribution = data_extractor.get_note_distribution_from_song_dict(song_dict)

    song_name=midifile[midifile.rfind("/")+1:]



    figure_comparison = plt.figure(figsize=(10,7))
    figure_comparison.suptitle('IDyOM Pitch prediction vs ground truth '+'('+folder_name+')')
    ax_prediction = figure_comparison.add_subplot(121)
    divider = make_axes_locatable(ax_prediction)
    ax_surprise = divider.append_axes("bottom", 1., pad=0.1, sharex=ax_prediction)

    ax_prediction = plot_pitch_distribution(ax_prediction,predicted_pitch_distribution,title='Pitch Prediction for '+song_name)
    ax_surprise = plot_surprise_across_time(ax_surprise,S,title='Surprise across time (darker = more surprise)')
    ax_surprise.yaxis.set_tick_params(labelleft=False)

    ax_ground_truth = figure_comparison.add_subplot(122)
    ax_ground_truth = plot_pitch_distribution(ax_ground_truth,pitch_distritbution,title='Ground Truth for '+song_name)
    divider_truth = make_axes_locatable(ax_ground_truth)
    ax_blank = divider_truth.append_axes("bottom", 1., pad=0.1, sharex=ax_ground_truth)
    ax_blank = plot_surprise_across_time(ax_blank,S*0)
    ax_blank.axis('off')

    figure_comparison.subplots_adjust()

    figure_comparison.savefig('/Users/guan/Desktop/matplotlib_figures/'+folder_name+'/'+song_name+'.png')


