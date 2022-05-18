"""
TODO:
1. ax_surprisal_along_property bug:
        secondary axis
2. surprisal_along_property_in_time
    currently not available

"""

import os
from typing import List

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from py2lispIDyOM.extract import MelodyInfo, ExperimentInfo


class BasicAxsGeneration:

    @staticmethod
    def generic_idyom_output_along_time(ax: matplotlib.axes.Axes,
                                        melody_info: MelodyInfo,
                                        selected_idyom_output: str,
                                        color=None):
        valid_property_list = melody_info.get_property_list()
        if selected_idyom_output in valid_property_list:
            selected_property_values = melody_info.access_properties([selected_idyom_output]).values.tolist()
            flatten_selected_property_values = [item for sublist in selected_property_values for item in sublist]
        else:
            raise ValueError(f'selected_idyom_output \'{selected_idyom_output}\' is invalid. '
                             f'Valid outputs are: {valid_property_list}')

        onset_values = np.int_(melody_info.access_properties(['onset']).values.tolist())
        onset_in_beat = onset_values / 24
        flatten_onset_in_beat = [item for sublist in onset_in_beat for item in sublist]
        ax.plot(flatten_onset_in_beat, flatten_selected_property_values, color=color)
        ax.margins(x=0.01)
        ax.margins(y=0)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xlabel('Time in beat')
        #    ax.xaxis.set_ticklabels([])  # hide xtick labels
        ax.set_ylabel(f'{selected_idyom_output}')
        ax.set_yscale('linear')
        return ax

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
        # ax.axis('image')
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
        # ax.axis('image')
        ax.title.set_text('Pitch Prediction')
        ax.set_xlabel('Time (beat)')
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

    @staticmethod
    def ax_surprisal_along_property(ax: matplotlib.axes.Axes,
                                    melody_info: MelodyInfo,
                                    selected_property: str,
                                    surprisal_source: str,
                                    # e.g., surprisal_source = 'cpitch' (meaning, get the cpitch.information.content)
                                    color=None):

        if surprisal_source == 'overall':
            formatted_surprisal_source = 'information.content'
        else:
            formatted_surprisal_source = surprisal_source + '.information.content'

        valid_surprisal_source = list(melody_info.keys()) + ['overall']
        valid_property_list = melody_info.get_property_list()

        # Access bottom x-axis ---> onset shown in beat
        onset_values = np.int_(melody_info.access_properties(['onset']))
        onset_in_beat = onset_values / 24
        flatten_onset_in_beat = [item for sublist in list(onset_in_beat) for item in sublist]

        # Access y-axis ---> surprisal_source
        if formatted_surprisal_source in melody_info.keys():
            surprisal_source_values = np.int_(melody_info.access_properties([formatted_surprisal_source]))
            flatten_surprisal_source_values = [item for sublist in list(surprisal_source_values) for item in sublist]
        else:
            raise ValueError(f'surprisal_source \'{surprisal_source}\' is invalid. '
                             f'Valid surprisal_source are \'{valid_surprisal_source}\'. ')

        # Access top x-axis ---> property values:
        if selected_property in valid_property_list:
            selected_property_values = np.int_(melody_info.access_properties([selected_property]))
            flatten_selected_property_values = np.array(
                [item for sublist in list(selected_property_values) for item in sublist])
        else:
            raise ValueError(f'selected_property \'{selected_property}\' is invalid. '
                             f'Valid properties are: {valid_property_list}')

        # ax.scatter(onset_in_beat, flatten_surprisal_source_values, color=color)
        # ax2 = ax.twiny()
        # ax2.scatter(flatten_selected_property_values, flatten_surprisal_source_values, color='green')
        #
        # ax.margins(x=0.03)
        # ax.margins(y=0.03)
        # # ax.spines['top'].set_visible(False)
        # ax.spines['right'].set_visible(False)
        #
        # ax.set_xticks(ticks=flatten_onset_in_beat)
        # ax.set_xticklabels(labels=flatten_onset_in_beat)
        # ax2.set_xticks(ticks=flatten_selected_property_values)
        # ax2.set_xticklabels(labels=flatten_selected_property_values)
        #
        # ax2.set_xlabel(f'{selected_property}')
        # ax.set_xlabel('onset')
        # ax.set_ylabel(f'{formatted_surprisal_source}')

        return ax


class Auxiliary:

    @staticmethod
    def batch_melodies_plots(plot_method_func,
                             fig_format: str,
                             dpi: float,
                             plot_type_folder_name: str,
                             experiment_folder_path: str,
                             melody_names: List[str] = None,
                             starting_index: int = None,
                             ending_index: int = None,
                             savefig: bool = True,
                             ):

        experiment_info = ExperimentInfo(experiment_folder_path=experiment_folder_path)
        all_melody_names = list(experiment_info.melodies_dict.keys())
        print(plot_type_folder_name)
        saved_msg = str('Plots saved in ' + experiment_folder_path + 'plots/' + str(plot_type_folder_name) + '/')

        def _common_batch_actions():
            melody_info = experiment_info.melodies_dict[melody]
            melody_name_pprint = melody_info.get_melody_name_pprint()
            fig = plot_method_func(melody_info)
            if savefig is True:
                Auxiliary.save_one_fig(plot_type_folder_name=plot_type_folder_name,
                                       experiment_folder_path=experiment_folder_path,
                                       melody_name_pprint=melody_name_pprint,
                                       fig=fig,
                                       fig_format=fig_format,
                                       dpi=dpi)
                print(saved_msg)

        if melody_names:
            for index, melody in enumerate(melody_names):
                _common_batch_actions()

        elif starting_index or ending_index:
            for index, melody in enumerate(all_melody_names[starting_index:ending_index]):
                _common_batch_actions()

        else:
            for index, melody in enumerate(all_melody_names):
                _common_batch_actions()

    @staticmethod
    def save_one_fig(plot_type_folder_name: str,
                     experiment_folder_path: str,
                     melody_name_pprint: str,
                     fig,
                     fig_format: str,
                     dpi: float):
        output_path = experiment_folder_path + 'plots/' + plot_type_folder_name + '/'
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        fig.savefig(fname=output_path + str(melody_name_pprint) + '.' + fig_format, format=fig_format, dpi=dpi)


class BasicPlot:

    @staticmethod
    def simple_plot(selected_idyom_output: str,
                    experiment_folder_path: str,
                    melody_names: List[str] = None,
                    starting_index: int = None,
                    ending_index: int = None,
                    savefig: bool = True,
                    showfig: bool = False,
                    fig_format: str = 'png',
                    dpi: float = 400,
                    figsize: tuple = (10, 5)):

        plot_type_folder_name = 'simple_plot_' + selected_idyom_output

        def _generic_property_along_time(melody_info: MelodyInfo,
                                         show_single_fig: bool = showfig) -> plt.Figure:

            melody_name_pprint = melody_info.get_melody_name_pprint()
            fig, (ax_generic_property) = plt.subplots(nrows=1, ncols=1, figsize=figsize, dpi=dpi, sharex='col')

            fig.suptitle('Selected IDyOM outputs: ' + selected_idyom_output + '\n\n Melody: ' + melody_name_pprint,
                         fontsize=15)
            BasicAxsGeneration.generic_idyom_output_along_time(ax_generic_property,
                                                               melody_info=melody_info,
                                                               selected_idyom_output=selected_idyom_output)
            plt.tight_layout()
            if show_single_fig is True:
                plt.show()
            else:
                pass
            return fig

        # Plot batch according to user inputs:
        Auxiliary.batch_melodies_plots(plot_method_func=_generic_property_along_time,
                                       plot_type_folder_name=plot_type_folder_name,
                                       experiment_folder_path=experiment_folder_path,
                                       melody_names=melody_names,
                                       starting_index=starting_index,
                                       ending_index=ending_index,
                                       savefig=savefig,
                                       fig_format=fig_format,
                                       dpi=dpi)

    @staticmethod
    def pianoroll_pitch_prediction_groundtruth(experiment_folder_path: str,
                                               melody_names: List[str] = None,
                                               starting_index: int = None,
                                               ending_index: int = None,
                                               savefig: bool = True,
                                               showfig: bool = False,
                                               fig_format: str = 'png',
                                               dpi: float = 400,
                                               nrows: int = 2,
                                               ncols: int = 1,
                                               figsize: tuple = (10, 10)):
        """
        This function returns and saves a pair of figures (the predicted pitch distribution and the ground truth) side by side.
        If users intend to plot figures for specific songs, they can do so by specifying either the melody names,
        or the starting/ending index in the melody list.

        :param nrows:
        :param ncols:
        :param figsize:
        :param dpi:
        :param fig_format:
        :param showfig:
        :param savefig:
        :param experiment_folder_path: the path to your experiment folder
        :param melody_names: if not supplied by the users,
        :param starting_index: the index of the melody in the melody list that you want to start plotting
        :param ending_index: the index of the melody in the melody list that you want to stop plotting
        :return:
        """
        plot_type_folder_name = 'pianoroll_pitch_prediction_groundtruth'

        def _pianoroll_pitch_prediction_groundtruth(melody_info: MelodyInfo,
                                                    show_single_fig: bool = showfig) -> plt.Figure:

            melody_name_pprint = melody_info.get_melody_name_pprint()

            fig, (ax_distribution, ax_groundtruth) = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize, dpi=dpi)
            fig.suptitle('IDyOM Pitch prediction vs ground truth \n\n Melody name: ' + melody_name_pprint)

            BasicAxsGeneration.pianoroll_pitch_distribution(ax_distribution, melody_info=melody_info)
            BasicAxsGeneration.pianoroll(ax_groundtruth, melody_info=melody_info)
            ax_groundtruth.title.set_text('Ground Truth')

            plt.tight_layout()

            if show_single_fig is True:
                plt.show()
            else:
                pass

            return fig

        Auxiliary.batch_melodies_plots(plot_method_func=_pianoroll_pitch_prediction_groundtruth,
                                       plot_type_folder_name=plot_type_folder_name,
                                       experiment_folder_path=experiment_folder_path,
                                       melody_names=melody_names,
                                       starting_index=starting_index,
                                       ending_index=ending_index,
                                       savefig=savefig,
                                       fig_format=fig_format,
                                       dpi=dpi
                                       )

    @staticmethod
    def pianoroll_groundtruth_overall_surprisal(experiment_folder_path: str,
                                                melody_names: List[str] = None,
                                                starting_index: int = None,
                                                ending_index: int = None,
                                                savefig: bool = True,
                                                showfig: bool = False,
                                                fig_format: str = 'png',
                                                dpi: float = 400,
                                                figsize: tuple = (10, 5)):
        """
        This function plots two axs: ground truth pianoroll on the top and the surprisal
        line plot on the bottom.
        :param figsize:
        :param fig_format:
        :param dpi:
        :param showfig:
        :param savefig:
        :param experiment_folder_path:
        :param melody_names:
        :param starting_index:
        :param ending_index:
        :return:
        """
        plot_type_folder_name = 'pianoroll_groundtruth_surprisal'

        def _pianoroll_groundtruth_surprisal(melody_info: MelodyInfo,
                                             show_single_fig: bool = showfig) -> plt.Figure:

            melody_name_pprint = melody_info.get_melody_name_pprint()

            fig, (ax_pianoroll, ax_surprisal) = plt.subplots(2, 1, figsize=figsize, dpi=dpi, sharex='col')
            fig.suptitle('IDyOM Information Content (Surprisal) \n\n Melody: ' + melody_name_pprint)

            BasicAxsGeneration.pianoroll(ax_pianoroll, melody_info=melody_info)
            BasicAxsGeneration.surprisal_continuous(ax_surprisal, melody_info=melody_info)

            plt.tight_layout()

            if show_single_fig is True:
                plt.show()
            else:
                pass
            return fig

        Auxiliary.batch_melodies_plots(plot_method_func=_pianoroll_groundtruth_surprisal,
                                       plot_type_folder_name=plot_type_folder_name,
                                       experiment_folder_path=experiment_folder_path,
                                       melody_names=melody_names,
                                       starting_index=starting_index,
                                       ending_index=ending_index,
                                       savefig=savefig,
                                       fig_format=fig_format,
                                       dpi=dpi)

    @staticmethod
    def surprisal_along_property_in_time(selected_property: str,
                                         surprisal_source: str,
                                         experiment_folder_path: str,
                                         melody_names: List[str] = None,
                                         starting_index: int = None,
                                         ending_index: int = None,
                                         savefig: bool = True,
                                         showfig: bool = False,
                                         fig_format: str = 'png',
                                         dpi: float = 400):

        """
        This function plots ...
        y-axis is the surprisal value (this can be either the 'overall' surprisal or the 'property' surprisal)
        x-axis is the property value

        :param dpi:
        :param fig_format:
        :param surprisal_source:
        :param selected_property:
        :param experiment_folder_path:
        :param melody_names:
        :param starting_index:
        :param ending_index:
        :param savefig:
        :param showfig:
        :return:
        """
        plot_type_folder_name = surprisal_source + '_surprisal_along_' + selected_property

        def _surprisal_along_property(melody_info: MelodyInfo,
                                      show_single_fig: bool = showfig) -> plt.Figure:
            melody_name_pprint = melody_info.get_melody_name_pprint()
            fig, (ax_surprisal_along_property) = plt.subplots(1, 1, figsize=(8, 5), dpi=dpi, sharex='col')

            fig.suptitle(
                surprisal_source + ' surprisal for ' + selected_property + '\n\n Melody: ' + melody_name_pprint,
                fontsize=15)
            BasicAxsGeneration.ax_surprisal_along_property(ax_surprisal_along_property,
                                                           melody_info=melody_info,
                                                           selected_property=selected_property,
                                                           surprisal_source=surprisal_source)

            plt.tight_layout()
            if show_single_fig is True:
                plt.show()
            else:
                pass
            return fig

        # Plot batch according to user inputs:

        Auxiliary.batch_melodies_plots(plot_method_func=_surprisal_along_property,
                                       plot_type_folder_name=plot_type_folder_name,
                                       experiment_folder_path=experiment_folder_path,
                                       melody_names=melody_names,
                                       starting_index=starting_index,
                                       ending_index=ending_index,
                                       savefig=savefig,
                                       fig_format=fig_format,
                                       dpi=dpi)
