"""
Viz arch:
---------

BasicPlot.single_plot(experiment_folder_path: str,
                      melody_names: List[str] = None,
                      starting_index: int = None,
                      ending_index: int = None
                      property_to_plot: Literal[str],)

TODO:
1. plot_overall_surprisal_entropy
2. plot any combinations of property surprisal

"""

import os
from typing import List

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from extraction import MelodyInfo, ExperimentInfo

"""
Plotting pitch prediction compare with ground truth
"""


class BasicAxsGeneration:

    @staticmethod
    def generic_property_along_time(ax: matplotlib.axes.Axes,
                                    melody_info: MelodyInfo,
                                    selected_property: str,
                                    color=None):
        valid_property_list = melody_info.get_property_list()
        if selected_property in valid_property_list:
            selected_property_values = np.int_(melody_info.access_properties([selected_property]))
        else:
            raise ValueError(f'selected_property \'{selected_property}\' is invalid. '
                             f'Valid properties are: {valid_property_list}')

        onset_values = np.int_(melody_info.access_properties(['onset']))
        ax.plot(onset_values, selected_property_values, color=color)
        ax.margins(x=0.01)
        ax.margins(y=0)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xlabel('Time')
        #    ax.xaxis.set_ticklabels([])  # hide xtick labels
        ax.set_ylabel(f'{selected_property}')

    @staticmethod
    def pianoroll(ax: matplotlib.axes.Axes,
                  melody_info: MelodyInfo):
        sustain_mask = melody_info.get_pianoroll_original()
        pitch_min, pitch_max = melody_info.parent_experiment.pitch_range
        duration_in_ticks = sustain_mask.shape[1]
        onsets = melody_info.access_properties(['onset']).to_numpy(dtype=int).reshape(-1)
        onsets_binary = np.zeros(duration_in_ticks)
        np.put(a=onsets_binary, ind=onsets, v=1)
        onsets_binary = onsets_binary.astype(bool)

        onsets_mask = onsets_binary * sustain_mask
        background_mask = np.bitwise_not(sustain_mask)

        colored_image = np.zeros(shape=sustain_mask.shape + (3,))
        colored_image[sustain_mask] = np.array([253, 231, 37])
        colored_image[onsets_mask] = np.array([59, 82, 139])
        colored_image[background_mask] = np.array([68, 1, 84])
        colored_image = colored_image.astype(int)

        ax.imshow(colored_image, origin='lower', aspect='auto',
                  extent=[0, duration_in_ticks / 24, pitch_min, pitch_max])
        ax.set_xlabel('Time (beat)')
        # ax.xaxis.set_ticklabels([])  # hide xtick labels
        ax.set_ylabel('Pitch (MIDI number)')
        return ax

    @staticmethod
    def pianoroll_pitch_distribution(ax: matplotlib.axes.Axes,
                                     melody_info: MelodyInfo):
        pitch_min, pitch_max = melody_info.parent_experiment.pitch_range
        duration_in_ticks = melody_info.get_pianoroll_original().shape[1]
        pianoroll_distribution_array = melody_info.get_pianoroll_pitch_distribution()
        ax.imshow(pianoroll_distribution_array, origin='lower', aspect='auto',
                  extent=[0, duration_in_ticks / 24, pitch_min, pitch_max])
        ax.title.set_text('Pitch Prediction')
        ax.set_xlabel('Time')
        # ax.xaxis.set_ticklabels([])  # hide xtick labels
        ax.set_ylabel('Pitch (MIDI number)')
        return ax

    @staticmethod
    def entropy(ax: matplotlib.axes.Axes,
                melody_info: MelodyInfo,
                color=None):

        entropy_values = np.int_(melody_info.access_properties(['entropy']))
        onset_values = np.int_(melody_info.access_properties(['onset']))
        ax.plot(onset_values, entropy_values, color=color)
        ax.margins(x=0.01)
        ax.margins(y=0)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xlabel('Time')
        #    ax.xaxis.set_ticklabels([])  # hide xtick labels
        ax.set_ylabel('Entropy')

        return ax

    @staticmethod
    def surprisal(ax: matplotlib.axes.Axes,
                  melody_info: MelodyInfo,
                  color=None):

        surprisal_values = np.int_(melody_info.access_properties(['information.content']))
        onset_values = np.int_(melody_info.access_properties(['onset']))
        ax.plot(onset_values, surprisal_values, color=color)
        ax.margins(x=0.01)
        ax.margins(y=0)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xlabel('Time')
        #   ax.xaxis.set_ticklabels([])  # hide xtick labels
        ax.set_ylabel('Information Content (Surprisal) \n -log(P)')
        return ax

    @staticmethod
    def surprisal_continuous(ax: matplotlib.axes.Axes,
                             melody_info: MelodyInfo,
                             color=None):

        # spike at onset
        surprisal_array = melody_info.get_surprisal_array()
        onset_time_vector = melody_info.get_onset_time_vector() / 24
        ax.plot(onset_time_vector, surprisal_array, color=color)
        ax.margins(x=0.01)
        ax.margins(y=0)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xlabel('Time (beat)')
        #    ax.xaxis.set_ticklabels([])  # hide xtick labels
        ax.set_ylabel('Information Content (Surprisal) \n -log(P)')
        return ax


class BasicPlot:

    @staticmethod
    def _aux_save_batch_plots(plot_method_func,
                              plot_type_folder_name: str,
                              experiment_folder_path: str,
                              melody_names: List[str] = None,
                              starting_index: int = None,
                              ending_index: int = None):

        experiment_info = ExperimentInfo(experiment_folder_path=experiment_folder_path)
        all_melody_names = list(experiment_info.melodies_dict.keys())
        print(plot_type_folder_name)
        saved_msg = str('Plots saved in' + experiment_folder_path + 'plots/' + str(plot_type_folder_name) + '/')

        if melody_names:
            for index, melody in enumerate(melody_names):
                melody_info = experiment_info.melodies_dict[melody]
                plot_method_func(melody_info)
            print(saved_msg)

        elif starting_index or ending_index:
            for index, melody in enumerate(all_melody_names[starting_index:ending_index]):
                melody_info = experiment_info.melodies_dict[melody]
                plot_method_func(melody_info)
            print(saved_msg)

        else:
            for index, melody in enumerate(all_melody_names):
                melody_info = experiment_info.melodies_dict[melody]
                plot_method_func(melody_info)
            print(saved_msg)

    @staticmethod
    def _aux_save_one_fig(plot_type_folder_name: str,
                          experiment_folder_path: str,
                          melody_name_pprint: str,
                          fig):
        output_path = experiment_folder_path + 'plots/' + plot_type_folder_name + '/'
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        fig.savefig(fname=output_path + str(melody_name_pprint) + '.eps', format='eps', dpi=400)

    @staticmethod
    def simple_plot(selected_property: str,
                    experiment_folder_path: str,
                    melody_names: List[str] = None,
                    starting_index: int = None,
                    ending_index: int = None):

        plot_type_folder_name = 'simple_plot_' + selected_property

        def _generic_property_along_time(melody_info: MelodyInfo) -> plt.Figure:
            melody_name_pprint = melody_info.get_melody_name_pprint()
            fig, (ax_generic_property) = plt.subplots(1, 1, figsize=(8, 5), dpi=400, sharex='col')

            fig.suptitle('Melody: ' + melody_name_pprint, fontsize=15)
            BasicAxsGeneration.generic_property_along_time(ax_generic_property,
                                                           melody_info=melody_info,
                                                           selected_property=selected_property)

            plt.tight_layout()

            BasicPlot._aux_save_one_fig(experiment_folder_path=experiment_folder_path,
                                        plot_type_folder_name=plot_type_folder_name,
                                        melody_name_pprint=melody_name_pprint,
                                        fig=fig)
            return fig

        BasicPlot._aux_save_batch_plots(plot_method_func=_generic_property_along_time,
                                        plot_type_folder_name=plot_type_folder_name,
                                        experiment_folder_path=experiment_folder_path,
                                        melody_names=melody_names,
                                        starting_index=starting_index,
                                        ending_index=ending_index)

    @staticmethod
    def single_plot(axes_modifier,
                    melody_info,
                    output_path) -> plt.Figure:

        melody_name = str(melody_info.access_properties(['melody.name']).to_numpy()[0][0]).replace('"', '')

        fig, ax = plt.subplots()
        axes_modifier(ax=ax, melody_info=melody_info)

        if not os.path.exists(output_path):
            os.makedirs(output_path)
        fig.savefig(fname=output_path + str(melody_name) + '.eps', format='eps', dpi=400)

        return fig

    @staticmethod
    def pianoroll_pitch_distribution_groundtruth(experiment_folder_path: str,
                                                 melody_names: List[str] = None,
                                                 starting_index: int = None,
                                                 ending_index: int = None):
        """
        This function returns and saves a pair of figures (the predicted pitch distribution and the ground truth) side by side.
        If users intend to plot figures for specific songs, they can do so by specifying either the melody names,
        or the starting/ending index in the melody list.

        :param experiment_folder_path: the path to your experiment folder
        :param melody_names: if not supplied by the users,
        :param starting_index: the index of the melody in the melody list that you want to start plotting
        :param ending_index: the index of the melody in the melody list that you want to stop plotting
        :return:
        """

        def pianoroll_pitch_distribution_groundtruth(melody_info: MelodyInfo) -> plt.Figure:
            melody_name = str(melody_info.access_properties(['melody.name']).to_numpy()[0][0]).replace('"', '')
            fig, (ax_distribution, ax_groundtruth) = plt.subplots(1, 2, figsize=(10, 5), dpi=400)
            fig.suptitle('IDyOM Pitch prediction vs ground truth \n\n Melody name: ' + melody_name)

            BasicAxsGeneration.pianoroll_pitch_distribution(ax_distribution, melody_info=melody_info)
            BasicAxsGeneration.pianoroll(ax_groundtruth, melody_info=melody_info)
            ax_groundtruth.title.set_text('Ground Truth')

            plt.tight_layout()

            output_path = experiment_folder_path + 'plots/pianoroll_pitch_distribution_groundtruth/'
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            fig.savefig(fname=output_path + str(melody_name) + '.eps', format='eps', dpi=400)

            return fig

        experiment_info = ExperimentInfo(experiment_folder_path=experiment_folder_path)
        all_melody_names = list(experiment_info.melodies_dict.keys())

        if melody_names:
            for index, melody in enumerate(melody_names):
                melody_info = experiment_info.melodies_dict[melody]
                pianoroll_pitch_distribution_groundtruth(melody_info)
            print('Plots saved in' + experiment_folder_path + 'plots/pianoroll_pitch_distribution_groundtruth/')

        elif starting_index or ending_index:
            for index, melody in enumerate(all_melody_names[starting_index:ending_index]):
                melody_info = experiment_info.melodies_dict[melody]
                pianoroll_pitch_distribution_groundtruth(melody_info)
            print('Plots saved in' + experiment_folder_path + 'plots/pianoroll_pitch_distribution_groundtruth/')

        else:
            for index, melody in enumerate(all_melody_names):
                melody_info = experiment_info.melodies_dict[melody]
                pianoroll_pitch_distribution_groundtruth(melody_info)
            print('Plots saved in: ' + experiment_folder_path + 'plots/pianoroll_pitch_distribution_groundtruth/')

    @staticmethod
    def pianoroll_groundtruth_surprisal(experiment_folder_path: str,
                                        melody_names: List[str] = None,
                                        starting_index: int = None,
                                        ending_index: int = None):
        """
        This function
        :param experiment_folder_path:
        :param melody_names:
        :param starting_index:
        :param ending_index:
        :return:
        """

        def _pianoroll_groundtruth_surprisal(melody_info: MelodyInfo) -> plt.Figure:
            melody_name_2print = str(melody_info.access_properties(['melody.name']).to_numpy()[0][0]).replace('"', '')
            fig, (ax_pianoroll, ax_surprisal) = plt.subplots(2, 1, figsize=(8, 5), dpi=400, sharex='col')

            fig.suptitle('Melody: ' + melody_name_2print, fontsize=15)
            BasicAxsGeneration.pianoroll(ax_pianoroll, melody_info=melody_info)
            BasicAxsGeneration.surprisal_continuous(ax_surprisal, melody_info=melody_info)

            plt.tight_layout()

            output_path = experiment_folder_path + 'plots/pianoroll_surprisal/'
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            fig.savefig(fname=output_path + str(melody_name_2print) + '.eps', format='eps', dpi=400)

            return fig

        experiment_info = ExperimentInfo(experiment_folder_path=experiment_folder_path)
        all_melody_names = list(experiment_info.melodies_dict.keys())

        if melody_names:
            for index, melody in enumerate(melody_names):
                melody_info = experiment_info.melodies_dict[melody]
                _pianoroll_groundtruth_surprisal(melody_info)
            print('Plots saved in' + experiment_folder_path + 'plots/pianoroll_surprisal/')

        elif starting_index or ending_index:
            for index, melody in enumerate(all_melody_names[starting_index:ending_index]):
                melody_info = experiment_info.melodies_dict[melody]
                _pianoroll_groundtruth_surprisal(melody_info)
            print('Plots saved in' + experiment_folder_path + 'plots/pianoroll_surprisal/')

        else:
            for index, melody in enumerate(all_melody_names):
                melody_info = experiment_info.melodies_dict[melody]
                _pianoroll_groundtruth_surprisal(melody_info)
            print('Plots saved in: ' + experiment_folder_path + 'plots/pianoroll_surprisal/')

    @staticmethod
    def line_plots_overall_surprisal_entropy(experiment_folder_path: str,
                                             melody_names: List[str] = None,
                                             starting_index: int = None,
                                             ending_index: int = None):

        def _line_plots_overall_surprisal_entropy(melody_info: MelodyInfo) -> plt.Figure:
            melody_name_2print = str(melody_info.access_properties(['melody.name']).to_numpy()[0][0]).replace('"', '')
            fig, (ax_surprisal, ax_entropy) = plt.subplots(2, 1, figsize=(8, 5), dpi=400, sharex='col')

            fig.suptitle('Melody: ' + melody_name_2print, fontsize=15)
            BasicAxsGeneration.surprisal(ax_surprisal, melody_info=melody_info)
            BasicAxsGeneration.entropy(ax_entropy, melody_info=melody_info)

            plt.tight_layout()

            output_path = experiment_folder_path + 'plots/overall_surprisal_entropy/'
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            fig.savefig(fname=output_path + str(melody_name_2print) + '.eps', format='eps', dpi=400)

            return fig

        experiment_info = ExperimentInfo(experiment_folder_path=experiment_folder_path)
        all_melody_names = list(experiment_info.melodies_dict.keys())

        if melody_names:
            for index, melody in enumerate(melody_names):
                melody_info = experiment_info.melodies_dict[melody]
                _line_plots_overall_surprisal_entropy(melody_info)
            print('Plots saved in' + experiment_folder_path + 'plots/overall_surprisal_entropy/')

        elif starting_index or ending_index:
            for index, melody in enumerate(all_melody_names[starting_index:ending_index]):
                melody_info = experiment_info.melodies_dict[melody]
                _line_plots_overall_surprisal_entropy(melody_info)
            print('Plots saved in' + experiment_folder_path + 'plots/overall_surprisal_entropy/')

        else:
            for index, melody in enumerate(all_melody_names):
                melody_info = experiment_info.melodies_dict[melody]
                _line_plots_overall_surprisal_entropy(melody_info)
            print('Plots saved in: ' + experiment_folder_path + 'plots/overall_surprisal_entropy/')


def func():
    experiment_folder_path = 'experiment_history/04-05-22_14.35.26/'

    # BasicPlot.line_plots_overall_surprisal_entropy(experiment_folder_path, ending_index=4)

    BasicPlot.simple_plot(selected_property='information.content',
                          experiment_folder_path=experiment_folder_path,
                          melody_names=['"shanx002"'])


if __name__ == '__main__':
    func()
