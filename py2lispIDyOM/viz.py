import os
from typing import List
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np

from py2lispIDyOM.extract import MelodyInfo, ExperimentInfo

# style customization:

matplotlib.rcParams['xtick.labelsize'] = 16
matplotlib.rcParams['ytick.labelsize'] = 16
matplotlib.rcParams['axes.labelsize'] = 16
matplotlib.rcParams['figure.titlesize'] = 20


class BasicAxsGeneration:

    @staticmethod
    def generic_idyom_output_along_time(ax: matplotlib.axes.Axes,
                                        melody_info: MelodyInfo,
                                        selected_idyom_output: str,
                                        grid: bool,
                                        color=None):
        valid_idyom_output_keyword_list = melody_info.get_idyom_output_keyword_list()
        if selected_idyom_output in valid_idyom_output_keyword_list:
            selected_output_values = melody_info.get_idyom_output_nparray(selected_idyom_output)
        else:
            raise ValueError(f'selected_idyom_output \'{selected_idyom_output}\' is invalid. '
                             f'Valid outputs are: {valid_idyom_output_keyword_list}')

        onset_in_beat = melody_info._get_onset_beat_nparray()

        ax.plot(onset_in_beat, selected_output_values, "-o", color=color)

        ax.margins(x=0.01)
        ax.margins(y=0)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        xticks = np.arange(0, np.amax(onset_in_beat))
        ax.set_xticks(ticks=xticks, minor=True)
        ax.set_xlabel('Time in quarter note')
        yticks = np.arange(0, np.amax(selected_output_values) + 1)
        ax.set_yticks(ticks=yticks, minor=True)
        ax.set_ylabel(f'{selected_idyom_output}')
        ax.set_yscale('linear')

        if grid is True:
            ax.grid(True)
        else:
            ax.grid(False)
        return ax

    @staticmethod
    def one_ic_along_onsets(ax: matplotlib.axes.Axes,
                            melody_info: MelodyInfo,
                            chosen_ic: str,  # type (e.g., 'cpitch.information.content')
                            grid: bool,
                            color: str,
                            yticks):

        onset_in_beat = melody_info._get_onset_beat_nparray()
        chosen_ic_values = melody_info.get_idyom_output_nparray(idyom_output_key=chosen_ic)

        ax.plot(onset_in_beat, chosen_ic_values, marker='o', label=chosen_ic, color=color, markersize=5)

        xticks = np.arange(0, np.amax(onset_in_beat))
        yticks = yticks + 1

        ax.set_xticks(ticks=xticks, minor=True)
        # ax.set_xlabel('Time in quarter note')
        ax.set_yticks(ticks=yticks, minor=True)
        ax.legend()

        if grid is True:
            ax.grid(True)
        else:
            ax.grid(False)
        return ax

    @staticmethod
    def one_entropy_along_onsets(ax: matplotlib.axes.Axes,
                                 melody_info: MelodyInfo,
                                 chosen_entropy: str,  # type (e.g., 'cpitch.information.content')
                                 grid: bool,
                                 color: str,
                                 yticks):

        onset_in_beat = melody_info._get_onset_beat_nparray()
        chosen_entropy_values = melody_info.get_idyom_output_nparray(idyom_output_key=chosen_entropy)

        ax.plot(onset_in_beat, chosen_entropy_values, marker='o', label=chosen_entropy, color=color, markersize=5)

        xticks = np.arange(0, np.amax(onset_in_beat))
        yticks = yticks + 1

        ax.set_xticks(ticks=xticks, minor=True)
        # ax.set_xlabel('Time in quarter note')
        ax.set_yticks(ticks=yticks, minor=True)
        ax.legend()

        if grid is True:
            ax.grid(True)
        else:
            ax.grid(False)
        return ax

    @staticmethod
    def selected_ic_entropy_along_onsets(ax: matplotlib.axes.Axes,
                                         melody_info: MelodyInfo,
                                         ic_source: str,
                                         entropy_source: str,
                                         grid: bool,
                                         ic_color=None,
                                         entropy_color=None,
                                         ):

        valid_keywords_list = melody_info.get_idyom_output_keyword_list()
        valid_surprisal_source = [keyword for keyword in valid_keywords_list if 'information.content' in keyword]
        valid_entropy_source = [keyword for keyword in valid_keywords_list if 'entropy' in keyword]

        # check usr inputs:
        if ic_source in valid_surprisal_source:
            ic_source_values = melody_info.access_idyom_output_keywords([ic_source]).values.tolist()
            flatten_ic_values = [item for sublist in ic_source_values for item in sublist]
        else:
            raise ValueError(f'ic_source \'{ic_source}\' is invalid. '
                             f'Valid information content source are: {valid_surprisal_source}')

        if entropy_source in valid_entropy_source:
            entropy_source_values = melody_info.access_idyom_output_keywords([entropy_source]).values.tolist()
            flatten_entropy_values = [item for sublist in entropy_source_values for item in sublist]
        else:
            raise ValueError(f'entropy_source \'{entropy_source}\' is invalid. '
                             f'Valid entropy source are: {valid_entropy_source}')

        onset_in_beat = melody_info._get_onset_beat_nparray()

        ax.plot(onset_in_beat, flatten_ic_values, "-o", label=ic_source, color=ic_color)
        ax.plot(onset_in_beat, flatten_entropy_values, "-o", label=entropy_source, color=entropy_color)

        max_ic = np.amax(flatten_ic_values)
        max_entropy = np.amax(flatten_entropy_values)

        xticks = np.arange(0, np.amax(onset_in_beat))
        yticks = np.arange(0, max(max_ic, max_entropy) + 1)

        ax.set_xticks(ticks=xticks, minor=True)
        ax.set_yticks(ticks=yticks, minor=True)
        ax.legend()
        if grid is True:
            ax.grid(True)
        else:
            ax.grid(False)
        #    ax.xaxis.set_ticklabels([])  # hide xtick labels
        # ax.set_ylabel(f'{ic_source}')

        return ax

    @staticmethod
    def pianoroll(ax: matplotlib.axes.Axes,
                  melody_info: MelodyInfo):
        sustain_mask = melody_info._get_pianoroll_original()

        pitch_min = np.amin(melody_info.exp_pitch_element_list)
        pitch_max = np.amax(melody_info.exp_pitch_element_list)

        duration_in_ticks = sustain_mask.shape[1]
        onsets = melody_info.access_idyom_output_keywords(['onset']).to_numpy(dtype=int).reshape(-1)
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

        # ax.axis('image')
        # ax.xaxis.set_ticklabels([])  # hide xtick labels
        ax.set_ylabel('Pitch (MIDI number)')
        ax = ax.imshow(colored_image, origin='lower', aspect='auto',
                       extent=[0, duration_in_ticks / 24, pitch_min, pitch_max])
        return ax

    @staticmethod
    def pianoroll_pitch_distribution(ax: matplotlib.axes.Axes,
                                     melody_info: MelodyInfo):
        pitch_min = np.amin(melody_info.exp_pitch_element_list)
        pitch_max = np.amax(melody_info.exp_pitch_element_list)

        duration_in_ticks = melody_info._get_pianoroll_original().shape[1]
        pianoroll_distribution_array = melody_info._get_pianoroll_pitch_distribution()
        ax.set_ylabel('Pitch (MIDI number)')
        ax = ax.imshow(pianoroll_distribution_array, origin='lower', aspect='auto',
                       extent=[0, duration_in_ticks / 24, pitch_min, pitch_max])

        return ax

    @staticmethod
    def ax_suprisal_colorbar(ax: matplotlib.axes.Axes,
                             melody_info: MelodyInfo,
                             color='viridis'):
        surprisal_values = melody_info.get_idyom_output_nparray('information.content')
        # print(surprisal_values)
        # extent = [min(surprisal_values), max(surprisal_values)]
        # ax.set_xticks(np.arange(*(extent + [1])), minor=True)
        ax.set_xlabel('Information content (surprisal) values')
        ax = ax.imshow(X=surprisal_values.reshape(1, -1), cmap=color, origin='lower')
        return ax

    @staticmethod
    def ax_blank_colorbar(ax: matplotlib.axes.Axes,
                          melody_info: MelodyInfo,
                          color='gray'):
        surprisal_values = melody_info.get_idyom_output_nparray('information.content')
        seq_len = len(surprisal_values)
        blank_seq = np.zeros(seq_len)
        ax = ax.imshow(X=blank_seq.reshape(1, -1), cmap=color, origin='lower')
        return ax

    @staticmethod
    def entropy(ax: matplotlib.axes.Axes,
                melody_info: MelodyInfo,
                color=None):

        entropy_values = melody_info.get_idyom_output_nparray('entropy')
        onset_values = melody_info.get_idyom_output_nparray('onset')
        ax.plot(onset_values, entropy_values, color=color)
        ax.margins(x=0.01)
        ax.margins(y=0)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xlabel("Time in quarter note")
        #    ax.xaxis.set_ticklabels([])  # hide xtick labels
        ax.set_ylabel('Entropy')

        return ax

    @staticmethod
    def surprisal(ax: matplotlib.axes.Axes,
                  melody_info: MelodyInfo,
                  color=None):

        surprisal_values = melody_info.get_idyom_output_nparray('information.content')
        onset_values = melody_info.get_idyom_output_nparray('onset')
        ax.plot(onset_values, surprisal_values, color=color)
        ax.margins(x=0.01)
        ax.margins(y=0)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_ylabel('Information Content (Surprisal) \n -log(P)')
        return ax

    @staticmethod
    def surprisal_continuous(ax: matplotlib.axes.Axes,
                             melody_info: MelodyInfo,
                             color=None):

        # spike at onset
        surprisal_array = melody_info._get_surprisal_array()
        onset_time_vector = melody_info._get_onset_time_vector() / 24
        ax.plot(onset_time_vector, surprisal_array, color=color)
        ax.margins(x=0.01)
        ax.margins(y=0)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # ax.set_xlabel('Time in quarter note')
        #    ax.xaxis.set_ticklabels([])  # hide xtick labels
        ax.set_ylabel('Information Content (Surprisal) \n -log(P)')
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
            melody_name_pprint = melody_info._get_melody_name_pprint()
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
    """ BasicPlot for selected IDyOM outputs in an experiment. """

    @staticmethod
    def pianoroll_pitch_prediction_groundtruth(experiment_folder_path: str,
                                               melody_names: List[str] = None,
                                               starting_index: int = None,
                                               ending_index: int = None,
                                               savefig: bool = True,
                                               showfig: bool = False,
                                               fig_format: str = 'png',
                                               dpi: float = 400,
                                               figsize: tuple = (10, 10),
                                               nrows: int = 2,
                                               ncols: int = 1,
                                               probability_colorbar: bool = False):

        """
        Generate a pair of figures (the predicted pitch distribution and the ground truth) side by side.
        If users intend to plot figures for specific songs, they can do so by specifying either the melody names,
        or the starting/ending index in the melody list.

        :param experiment_folder_path: The path to your experiment folder.
        :param melody_names: (optional), if not supplied by the users, default is all test melodies in the experiment.
        :param starting_index: (optional), the index of the melody in the melody list that you want to start plotting.
        :param ending_index: (optional), the index of the melody in the melody list that you want to stop plotting.
        :param savefig: (optional)
        :param showfig: (optional)
        :param fig_format: (optional), default = 'png
        :param dpi: (optional), default = 400
        :param figsize: (optional), default is (10,5)
        :param ncols: (optional), the number of columns of the figure. By default, ncols = 2, nrows = 1, figures are shown side-by-side.
        :param nrows: (optional), the number of columns of the figure. By default, ncols = 2, nrows = 1, figures are shown side-by-side.
        :param probability_colorbar: (optional) whether to show the color bar for the probabilities of the predict pitch or not.
        """

        plot_type_folder_name = 'pianoroll_pitch_prediction_groundtruth'

        def _pianoroll_pitch_prediction_groundtruth(melody_info: MelodyInfo,
                                                    show_single_fig: bool = showfig,
                                                    probability_colorbar: bool = probability_colorbar) -> plt.Figure:

            melody_name_pprint = melody_info._get_melody_name_pprint()

            fig, (ax_distribution, ax_groundtruth) = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize, dpi=dpi)
            fig.subplots_adjust(wspace=0.03)
            fig.suptitle('IDyOM Pitch prediction vs Ground truth \n\n Melody name: ' + melody_name_pprint)

            distribution = BasicAxsGeneration.pianoroll_pitch_distribution(ax_distribution, melody_info=melody_info)
            groundtruth = BasicAxsGeneration.pianoroll(ax_groundtruth, melody_info=melody_info)

            if probability_colorbar is True:
                distribution_divider = make_axes_locatable(ax_distribution)
                ax_surprise = distribution_divider.append_axes("right", size="3%", pad=0.1)
                cb_surprisal = fig.colorbar(distribution, cax=ax_surprise)
                cb_surprisal.set_label('Probabilities of predicted pitches')

                truth_divider = make_axes_locatable(ax_groundtruth)
                ax_blank = truth_divider.append_axes("right", size="3%", pad=0.1)
                # cb_blank = fig.colorbar(groundtruth, cax=ax_blank)
                ax_blank.axis('off')
            else:
                pass

            fig.supxlabel("Time in quarter note")
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
                                                figsize: tuple = (10, 6)):
        """
        Generate a pair of figures: ground truth piano roll on the top and the surprisal line plot on the bottom.

        :param experiment_folder_path: the path to your experiment folder.
        :param melody_names: (optional), if not supplied by the users, default is all test melodies in the experiment.
        :param starting_index: (optional),the index of the melody in the melody list that you want to start plotting.
        :param ending_index: (optional), the index of the melody in the melody list that you want to stop plotting.
        :param savefig: (optional)
        :param showfig: (optional)
        :param fig_format: (optional), default = 'png'
        :param dpi: (optional), default = 400
        :param figsize: (optional), default is (10,5)

        """

        plot_type_folder_name = 'pianoroll_groundtruth_surprisal'

        def _pianoroll_groundtruth_surprisal(melody_info: MelodyInfo,
                                             show_single_fig: bool = showfig) -> plt.Figure:

            melody_name_pprint = melody_info._get_melody_name_pprint()

            fig, (ax_pianoroll, ax_surprisal) = plt.subplots(2, 1, figsize=figsize, dpi=dpi, sharex='col')
            fig.subplots_adjust(wspace=0.03)
            fig.suptitle('IDyOM Information Content (Surprisal) \n\n Melody: ' + melody_name_pprint)

            BasicAxsGeneration.pianoroll(ax_pianoroll, melody_info=melody_info)
            BasicAxsGeneration.surprisal_continuous(ax_surprisal, melody_info=melody_info)

            fig.supxlabel("Time in quarter note")
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
    def simple_plot(selected_idyom_output: str,
                    experiment_folder_path: str,
                    melody_names: List[str] = None,
                    starting_index: int = None,
                    ending_index: int = None,
                    savefig: bool = True,
                    showfig: bool = False,
                    fig_format: str = 'png',
                    dpi: float = 400,
                    figsize: tuple = (10, 5),
                    grid: bool = True,
                    ggplot: bool = True):
        """
        Generate a simple line plot with time (in quarter note) on the x-axis, and selected IDyOM output on the y-axis.

        :param selected_idyom_output: the keyword of the IDyOM output you want to plot.
        :param experiment_folder_path: the path to your experiment folder.
        :param melody_names: if not supplied by the users, default is all test melodies in the experiment.
        :param starting_index: the index of the melody in the melody list that you want to start plotting.
        :param ending_index: the index of the melody in the melody list that you want to stop plotting.
        :param savefig:
        :param showfig:
        :param fig_format: default = 'png
        :param dpi: optional, default = 400
        :param figsize: optional, default is (10,5)
        :param grid: whether to show grid or not.
        :param ggplot: whether to use ggplot or not.

        """
        plot_type_folder_name = 'simple_plot_' + selected_idyom_output

        def _generic_property_along_time(melody_info: MelodyInfo,
                                         show_single_fig: bool = showfig,
                                         grid: bool = grid,
                                         ggplot: bool = ggplot) -> plt.Figure:

            if ggplot is True:
                plt.style.use('ggplot')
            else:
                pass

            melody_name_pprint = melody_info._get_melody_name_pprint()
            fig, (ax_generic_property) = plt.subplots(nrows=1, ncols=1, figsize=figsize, dpi=dpi, sharex='col')

            fig.suptitle('Selected IDyOM outputs: ' + selected_idyom_output + '\n\n Melody: ' + melody_name_pprint)
            BasicAxsGeneration.generic_idyom_output_along_time(ax_generic_property,
                                                               melody_info=melody_info,
                                                               selected_idyom_output=selected_idyom_output,
                                                               grid=grid)
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
    def selected_surprisal_entropy(experiment_folder_path: str,
                                   ic_source: str,
                                   entropy_source: str,
                                   melody_names: List[str] = None,
                                   starting_index: int = None,
                                   ending_index: int = None,
                                   savefig: bool = True,
                                   showfig: bool = False,
                                   fig_format: str = 'png',
                                   dpi: float = 400,
                                   figsize: tuple = (10, 6),
                                   grid: bool = True,
                                   ggplot: bool = True):
        """
        Generate a figure that shows the selected entropy and information content.

        :param experiment_folder_path: the path to your experiment folder.
        :param entropy_source: the source of entropy.
        :param ic_source: the source of information content (surprisal)
        :param melody_names: if not supplied by the users, default is all test melodies in the experiment.
        :param starting_index: the index of the melody in the melody list that you want to start plotting.
        :param ending_index: the index of the melody in the melody list that you want to stop plotting.
        :param savefig:
        :param showfig:
        :param fig_format: default = 'png
        :param dpi: default = 400
        :param figsize: default is (10,5)
        :param grid: whether to show grid or not.
        :param ggplot: whether to use ggplot or not.

        """

        plot_type_folder_name = 'selected_surprisal_entropy'

        def _selected_surprisal_entropy(melody_info: MelodyInfo,
                                        ic_source: str = ic_source,
                                        entropy_source: str = entropy_source,
                                        show_single_fig: bool = showfig,
                                        grid: bool = grid,
                                        ggplot: bool = ggplot) -> plt.Figure:

            if ggplot is True:
                plt.style.use('ggplot')
            else:
                pass
            melody_name_pprint = melody_info._get_melody_name_pprint()
            fig, ax = plt.subplots(figsize=figsize)
            fig.suptitle('IDyOM Information Content (Surprisal) and Entropy \n\n Melody: ' + melody_name_pprint)

            BasicAxsGeneration.selected_ic_entropy_along_onsets(ax=ax,
                                                                melody_info=melody_info,
                                                                ic_source=ic_source,
                                                                entropy_source=entropy_source,
                                                                ic_color='C0',
                                                                entropy_color='C1',
                                                                grid=grid)
            fig.supxlabel('Time in quarter note')
            fig.supylabel('Surprisal or entropy values')
            plt.tight_layout()

            if show_single_fig is True:
                plt.show()
            else:
                pass
            return fig

        Auxiliary.batch_melodies_plots(plot_method_func=_selected_surprisal_entropy,
                                       plot_type_folder_name=plot_type_folder_name,
                                       experiment_folder_path=experiment_folder_path,
                                       melody_names=melody_names,
                                       starting_index=starting_index,
                                       ending_index=ending_index,
                                       savefig=savefig,
                                       fig_format=fig_format,
                                       dpi=dpi)

    @staticmethod
    def all_surprisal(experiment_folder_path: str,
                      melody_names: List[str] = None,
                      starting_index: int = None,
                      ending_index: int = None,
                      savefig: bool = True,
                      showfig: bool = False,
                      fig_format: str = 'png',
                      dpi: float = 400,
                      figsize: tuple = (10, 8),
                      grid: bool = True,
                      ggplot: bool = True):
        """
        Generate subplots of all available surprisal outputs.

        :param experiment_folder_path: the path to your experiment folder.
        :param melody_names: if not supplied by the users, default is all test melodies in the experiment.
        :param starting_index: the index of the melody in the melody list that you want to start plotting.
        :param ending_index: the index of the melody in the melody list that you want to stop plotting.
        :param savefig:
        :param showfig:
        :param fig_format: default = 'png
        :param dpi: default = 400
        :param figsize: default is (10,5)
        :param grid: whether to show grid or not.
        :param ggplot: whether to use ggplot or not.

        """

        plot_type_folder_name = 'surprisals_plots'

        def _all_surprisal_plots(melody_info: MelodyInfo,
                                 grid: bool = grid,
                                 show_single_fig: bool = showfig,
                                 figsize: tuple = figsize,
                                 dpi: float = dpi,
                                 ggplot: bool = ggplot) -> plt.Figure:

            if ggplot is True:
                plt.style.use('ggplot')
            else:
                pass

            melody_name_pprint = melody_info._get_melody_name_pprint()

            valid_keywords_list = melody_info.get_idyom_output_keyword_list()
            all_surprisal_sources = [keyword for keyword in valid_keywords_list if 'information.content' in keyword]

            num_of_surprisal_subplots = len(all_surprisal_sources)
            # to get the same y-range for all plots (0, max_surprisal across all surprisals)
            max_surprisals = []
            for idx, surprisal_source in enumerate(all_surprisal_sources):
                surprisals = np.amax(melody_info.get_idyom_output_nparray(surprisal_source))
                max_surprisals.append(surprisals)
            yticks = np.arange(0, max(max_surprisals))

            # plot a number of surprisal plots stacked one on top of each other, shared x, y
            # add every single subplot to the figure with a for loop
            fig, axs = plt.subplots(num_of_surprisal_subplots, figsize=figsize, dpi=dpi, sharex='col', sharey='row')
            fig.subplots_adjust(wspace=0.03)
            fig.suptitle('IDyOM Information Content (Surprisal) \n\n Melody: ' + melody_name_pprint)

            for idx, surprisal_type in enumerate(all_surprisal_sources):
                BasicAxsGeneration.one_ic_along_onsets(ax=axs[idx],
                                                       melody_info=melody_info,
                                                       chosen_ic=surprisal_type,
                                                       grid=grid,
                                                       color=str('C' + str(idx)),
                                                       yticks=yticks)

            fig.supxlabel("Time in quarter note")
            fig.supylabel(t='Information Content (Surprisal)\n-log(P)', x=0.04, ha='center')

            plt.tight_layout()
            plt.style.use('ggplot')

            if show_single_fig is True:
                plt.show()
            else:
                pass
            return fig

        Auxiliary.batch_melodies_plots(plot_method_func=_all_surprisal_plots,
                                       plot_type_folder_name=plot_type_folder_name,
                                       experiment_folder_path=experiment_folder_path,
                                       melody_names=melody_names,
                                       starting_index=starting_index,
                                       ending_index=ending_index,
                                       savefig=savefig,
                                       fig_format=fig_format,
                                       dpi=dpi)

    @staticmethod
    def all_entropy(experiment_folder_path: str,
                    melody_names: List[str] = None,
                    starting_index: int = None,
                    ending_index: int = None,
                    savefig: bool = True,
                    showfig: bool = False,
                    fig_format: str = 'png',
                    dpi: float = 400,
                    figsize: tuple = (10, 8),
                    grid: bool = True,
                    ggplot: bool = True):
        """
        Generate subplots that show all available entropy outputs.

        :param experiment_folder_path: the path to your experiment folder.
        :param melody_names: if not supplied by the users, default is all test melodies in the experiment.
        :param starting_index: the index of the melody in the melody list that you want to start plotting.
        :param ending_index: the index of the melody in the melody list that you want to stop plotting.
        :param savefig:
        :param showfig:
        :param fig_format: default = 'png
        :param dpi: default = 400
        :param figsize: default is (10,5)
        :param grid: whether to show grid or not.
        :param ggplot: whether to use ggplot or not.

        """

        plot_type_folder_name = 'entropy_plots'

        def _all_entropy_plots(melody_info: MelodyInfo,
                               grid: bool = grid,
                               show_single_fig: bool = showfig,
                               figsize: tuple = figsize,
                               dpi: float = dpi,
                               ggplot: bool = ggplot) -> plt.Figure:

            if ggplot is True:
                plt.style.use('ggplot')
            else:
                pass

            melody_name_pprint = melody_info._get_melody_name_pprint()

            valid_keywords_list = melody_info.get_idyom_output_keyword_list()
            all_entropy_sources = [keyword for keyword in valid_keywords_list if 'entropy' in keyword]

            num_of_surprisal_subplots = len(all_entropy_sources)
            # to get the same y-range for all plots (0, max_surprisal across all surprisals)
            max_entropys = []
            for idx, entropy_source in enumerate(all_entropy_sources):
                entropys = np.amax(melody_info.get_idyom_output_nparray(entropy_source))
                max_entropys.append(entropys)
            yticks = np.arange(0, max(max_entropys))

            # plot a number of entropy plots stacked one on top of each other, shared x, y
            # add every single subplot to the figure with a for loop
            fig, axs = plt.subplots(num_of_surprisal_subplots, figsize=figsize, dpi=dpi, sharex='col', sharey='row')
            fig.suptitle('IDyOM Entropy \n\n Melody: ' + melody_name_pprint)

            for idx, entropy_type in enumerate(all_entropy_sources):
                BasicAxsGeneration.one_entropy_along_onsets(ax=axs[idx],
                                                            melody_info=melody_info,
                                                            chosen_entropy=entropy_type,
                                                            grid=grid,
                                                            color=str('C' + str(idx)),
                                                            yticks=yticks)

            plt.xlabel("Time in quarter note")
            plt.tight_layout()
            plt.style.use('ggplot')

            if show_single_fig is True:
                plt.show()
            else:
                pass
            return fig

        Auxiliary.batch_melodies_plots(plot_method_func=_all_entropy_plots,
                                       plot_type_folder_name=plot_type_folder_name,
                                       experiment_folder_path=experiment_folder_path,
                                       melody_names=melody_names,
                                       starting_index=starting_index,
                                       ending_index=ending_index,
                                       savefig=savefig,
                                       fig_format=fig_format,
                                       dpi=dpi)
