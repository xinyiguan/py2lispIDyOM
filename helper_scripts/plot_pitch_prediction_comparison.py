"""
This script is to make the comparison figure(s) of the predicted pitch distributions and ground truth pitches.
The plots does not show the actual duration of the notes. The horizontal axis refers to the time step of the notes.
"""

import numpy as np
import matplotlib.pyplot as plt
from helper_scripts import data_extractor
from mpl_toolkits.axes_grid1 import make_axes_locatable
from configuration import configurations
from glob import glob
import os


def get_pitch_distribution_from_sequence(pitch_sequence, pitch_range):
    """
    one-hot encode {ground truth pitch sequence} to {pitch distribution sequence}
    """
    pitch_sequence = np.array(pitch_sequence).reshape(-1,1)
    f = lambda x,y:(x,y+1)
    options = np.arange(*f(*pitch_range))
    distribution = pitch_sequence == options
    return distribution


def plot_pitch_distribution(ax, pitch_distribution, title, pitch_range):
    ax.set_xlabel('Time step')
    ax.set_ylabel('Pitch (MIDI number)')
    ax.set_title(title)
    x_extent = [0, pitch_distribution.shape[0]]
    y_extent = list(pitch_range)
    ax.set_xticks(np.arange(*(x_extent+[1])), minor=True)
    ax.set_yticks(np.arange(*(y_extent+[1])), minor=True)
    ax.imshow(pitch_distribution.T, origin='lower', extent=[0, pitch_distribution.shape[0]] + list(pitch_range))
    return ax

def plot_surprise_across_time(ax,surprise_across_time,title=None):
    x_extent = [0, surprise_across_time.shape[0]]
    ax.set_xticks(np.arange(*(x_extent + [1])), minor=True)
    ax.set_xlabel(title)
    ax.imshow(surprise_across_time.reshape(1, -1), cmap='Greys', interpolation='gaussian', origin='lower', extent= x_extent+[0, 1])
    return ax


def make_comparison_figure_from_index(song_index,all_song_dict, pitch_range,output_path):
    song_dict_of_interest = list(all_song_dict.values())[song_index]
    surprise = data_extractor.get_surprise_from_song_dict(song_dict_of_interest)
    ground_truth_pitch_sequence_from_song_dict = data_extractor.get_pitch_from_song_dict(song_dict_of_interest)
    ground_truth_pitch_distribution_from_song_dict = get_pitch_distribution_from_sequence(ground_truth_pitch_sequence_from_song_dict, pitch_range)
    predicted_pitch_distribution = data_extractor.get_pitch_distribution_from_song_dict(song_dict_of_interest)
    melody_name = str(data_extractor.get_melody_name_from_song_dict(song_dict_of_interest))
    experiment_name = configurations['experiment_name']

    figure_comparison = plt.figure(figsize=(10,8))
    figure_comparison.suptitle('IDyOM Pitch prediction vs ground truth '+'('+experiment_name+')'+ '\n\nMelody: ' + melody_name +'\n\n')
    ax_prediction = figure_comparison.add_subplot(121)
    divider = make_axes_locatable(ax_prediction)
    ax_surprise = divider.append_axes("bottom", 1., pad=0.1, sharex=ax_prediction)

    ax_prediction = plot_pitch_distribution(ax_prediction, predicted_pitch_distribution, title='Pitch Prediction', pitch_range=pitch_range)
    ax_surprise = plot_surprise_across_time(ax_surprise, surprise ,title='Surprise across time (darker = more surprise)')
    ax_surprise.yaxis.set_tick_params(labelleft=False)

    ax_ground_truth = figure_comparison.add_subplot(122)
    ax_ground_truth = plot_pitch_distribution(ax_ground_truth, ground_truth_pitch_distribution_from_song_dict ,title='Ground Truth ', pitch_range=pitch_range)
    divider_truth = make_axes_locatable(ax_ground_truth)
    ax_blank = divider_truth.append_axes("bottom", 1., pad=0.1, sharex=ax_ground_truth)
    ax_blank = plot_surprise_across_time(ax_blank, surprise*0)
    ax_blank.axis('off')
    figure_comparison.subplots_adjust(wspace=0)
    plt.tight_layout()

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    figure_comparison.savefig(output_path + str(melody_name) + '.eps')



## If run this module only:

def make_comparison_figure_from_history_folder(selected_experiment_history_folder):
    dat_file_path = sorted(glob(selected_experiment_history_folder + 'experiment_output_data_folder/*'))[0]
    all_song_dict = data_extractor.get_all_song_dict_from_dat(dat_file_path)
    num_of_songs_in_dict = len(all_song_dict.keys())
    pitch_range = (47, 91)

    # current_iteration_range = range(5600, 7021)
    # for i in current_iteration_range:
    for i in range(num_of_songs_in_dict):
        print('processing song ' + str(i+1) + '/' +str(num_of_songs_in_dict))
        make_comparison_figure_from_index(i,all_song_dict, pitch_range,output_path=selected_experiment_history_folder + 'plot_pitch_prediction_comparison/')
    print('Plots are saved in plot_pitch_prediction_comparison folder!')

if __name__ == '__main__':
    selected_experiment_history_folder = '/Users/xinyiguan/NewMac_LocalProjectFolders/experiment_history/midi5_03-06-21_22.42.36/'
    make_comparison_figure_from_history_folder(selected_experiment_history_folder)