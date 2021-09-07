"""Convenience functions for plotting."""


import numpy as np
import matplotlib.pyplot as plt
from helper_scripts import data_extractor
from mpl_toolkits.axes_grid1 import make_axes_locatable
from configuration import configurations
import os
from glob import glob



"""
Plotting pitch prediction compare with ground truth
"""

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

def plot_surprisal_bar_across_time(ax,surprise_across_time,title=None):
    x_extent = [0, surprise_across_time.shape[0]]
    ax.set_xticks(np.arange(*(x_extent + [1])), minor=True)
    ax.set_xlabel(title)
    ax.imshow(surprise_across_time.reshape(1, -1), cmap='Greys', interpolation='gaussian', origin='lower', extent= x_extent+[0, 1])
    return ax


def make_comparison_figure_from_index(song_index,all_song_dict, pitch_range,output_path):
    song_dict_of_interest = list(all_song_dict.values())[song_index]
    surprise = data_extractor.get_overall_information_content_from_song_dict(song_dict_of_interest)
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
    ax_surprise = plot_surprisal_bar_across_time(ax_surprise, surprise ,title='Surprisal across time (darker = more surprise)')
    ax_surprise.yaxis.set_tick_params(labelleft=False)

    ax_ground_truth = figure_comparison.add_subplot(122)
    ax_ground_truth = plot_pitch_distribution(ax_ground_truth, ground_truth_pitch_distribution_from_song_dict ,title='Ground Truth ', pitch_range=pitch_range)
    divider_truth = make_axes_locatable(ax_ground_truth)
    ax_blank = divider_truth.append_axes("bottom", 1., pad=0.1, sharex=ax_ground_truth)
    ax_blank = plot_surprisal_bar_across_time(ax_blank, surprise*0)
    ax_blank.axis('off')
    figure_comparison.subplots_adjust(wspace=0)
    plt.tight_layout()

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    figure_comparison.savefig(output_path + str(melody_name).replace('"', '') + '.eps')



def make_comparison_figure_from_history_folder(selected_experiment_history_folder):
    dat_file_path = sorted(glob(selected_experiment_history_folder + 'experiment_output_data_folder/*'))[0]
    all_song_dict = data_extractor.get_all_song_dict_from_dat(dat_file_path)
    num_of_songs_in_dict = len(all_song_dict.keys())
    pitch_range = (47, 91)

    # current_iteration_range = range(5600, 7021)
    # for i in current_iteration_range:
    for i in range(num_of_songs_in_dict):
        print('processing song ' + str(i+1) + '/' +str(num_of_songs_in_dict))
        make_comparison_figure_from_index(i,all_song_dict, pitch_range,output_path=selected_experiment_history_folder + 'viz_pitch_prediction_comparison/')
    print('Plots are saved in plot_pitch_prediction_comparison folder!')







"""
Make the figure(s) of surprise values aligned with piano roll reference.
"""

def get_pianoroll_with_duration_from_sequence(song_index,all_song_dict,pitch_range):
    """
    This function takes a pitch sequence and duration sequence (np.arrays) from the song of choice,
    and outputs a pianoroll matrix with duration encoded

    one-hot encode {ground truth pitch sequence} to {pitch distribution sequence}
    """
    song_dict_of_interest = list(all_song_dict.values())[song_index]
    pitch_sequence = data_extractor.get_pitch_from_song_dict(song_dict_of_interest)
    pitch_sequence = np.array(pitch_sequence).reshape(-1,1)
    f = lambda x,y:(x,y+1)
    options = np.arange(*f(*pitch_range))
    distribution = pitch_sequence == options

    duration_sequence = data_extractor.get_duration_from_song_dict(song_dict_of_interest)
    def duplicate_pitch_distr_column(column, n):
        column = np.expand_dims(column,0)
        columns = np.repeat(column, n, axis=0)
        return columns
    bundles = []
    for i,column in enumerate(distribution):
        n = duration_sequence[i]/6
        bundle = duplicate_pitch_distr_column(column, n)
        bundles.append(bundle)
    piano_roll_with_duration = np.concatenate(tuple(bundles))
    return piano_roll_with_duration

def plot_ground_truth_pianoroll_with_duration(ax,all_song_dict, song_index,pitch_range):
    """
    Plot the ground truth pianoroll with duration.
    This function creates axes of the ground truth pianoroll plot.
    """

    song_dict_of_interest = list(all_song_dict.values())[song_index]
    melody_name = data_extractor.get_melody_name_from_song_dict(song_dict_of_interest)
    ax.set_title('Song: ' + str(melody_name))
    #ax.set_xlabel('Time')
    ax.set_ylabel('Pitch (MIDI number)')
    pitch_distribution = get_pianoroll_with_duration_from_sequence(song_index,all_song_dict, pitch_range)
    pitch_distribution = np.pad(pitch_distribution,(1,0),'constant')
    x_extent = [-1, pitch_distribution.shape[0]-1]
    y_extent = list(pitch_range)
    # ax.set_xticks(np.arange(*(x_extent+[1])),minor = True)
    # ax.set_yticks(np.arange(*(y_extent+[1])),minor = True)
    ax.imshow(pitch_distribution.T, origin ='lower', extent= x_extent + y_extent, aspect='auto')
    return ax


def plot_surprisal_across_time(ax, song_index, all_song_dict):
    """
    Plot the surprise values across time (stem plot).
    This function creates the axes for the surprise plot.
    """
    song_dict_of_interest = list(all_song_dict.values())[song_index]
    ax.set_xlabel('Time (in 16th note)')
    ax.set_ylabel('Surprise -log(P)')
    onset_sequence = data_extractor.get_onset_from_song_dict(song_dict_of_interest)
    surprise_sequence = data_extractor.get_overall_information_content_from_song_dict(song_dict_of_interest)
    x = onset_sequence/6
    y = surprise_sequence
    # ax.stem(x,y, linefmt ='grey', bottom=-1, markerfmt='C7o')

    markerline, stemline, baseline, = ax.stem(x, y, linefmt='grey', markerfmt='C7o', basefmt='k.')
    plt.setp(stemline, linewidth=1.25)
    plt.setp(markerline, markersize=3)

    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=-1)
    return ax


def make_pianoroll_surprise_figure_from_index(song_index, all_song_dict,pitch_range,output_path):
    """
    This function makes a figure that contains two subplots: ground truth pianoroll and the corresponding surprises.
    """

    song_dict_of_interest = list(all_song_dict.values())[song_index]
    melody_name = data_extractor.get_melody_name_from_song_dict(song_dict_of_interest)

    single_song_fig, (ax_ground_truth, ax_surprise) = plt.subplots(2, 1, sharex=True)
    single_song_fig.set_size_inches(12, 7)
    single_song_fig.suptitle('IDyOM - Surprise values aligned with piano roll', fontsize=16)
    ax_ground_truth = plot_ground_truth_pianoroll_with_duration(ax_ground_truth, song_index=song_index,all_song_dict=all_song_dict,pitch_range=pitch_range)
    ax_surprise = plot_surprisal_across_time(ax_surprise, song_index,all_song_dict)
    single_song_fig.subplots_adjust(hspace=0)
    plt.tight_layout()

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    single_song_fig.savefig(output_path + str(melody_name).replace('"', '')+ '.eps')


def make_pianoroll_surprise_figure_from_history_folder(selected_experiment_history_folder):
    dat_file_path = sorted(glob(selected_experiment_history_folder + 'experiment_output_data_folder/*'))[0]
    all_song_dict = data_extractor.get_all_song_dict_from_dat(dat_file_path)
    num_of_songs_in_dict = len(all_song_dict.keys())
    pitch_range = (47, 91)

    # current_iteration_range = range(5600, 7021)
    # for i in current_iteration_range:
    for i in range(num_of_songs_in_dict):
        print('processing song ' + str(i+1) + '/' +str(num_of_songs_in_dict))
        make_pianoroll_surprise_figure_from_index(i,all_song_dict,pitch_range,output_path=selected_experiment_history_folder + 'viz_surprisal_with_pianoroll/')
    print('Plots are saved in viz_surprisal_with_pianoroll folder!')



if __name__ == '__main__':
    selected_experiment_history_folder = '/Users/xinyiguan/Desktop/Codes/IDyOM_Python_Interface/experiment_history/03-08-21_13.40.14/'
    make_comparison_figure_from_history_folder(selected_experiment_history_folder)
    make_pianoroll_surprise_figure_from_history_folder(selected_experiment_history_folder)