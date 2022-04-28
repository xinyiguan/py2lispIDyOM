"""
viz module v2 - March 2022
"""
import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from extraction import MelodyInfo, ExperimentInfo

"""
Plotting pitch prediction compare with ground truth
"""


class BasicAxsGeneration:

    @staticmethod
    def pianoroll(ax: matplotlib.axes.Axes, melody_info: MelodyInfo):
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
    def pianoroll_pitch_distribution(ax: matplotlib.axes.Axes, melody_info: MelodyInfo):
        pianoroll_distribution_array = melody_info.get_pianoroll_pitch_distribution()
        ax.imshow(pianoroll_distribution_array, origin='lower', aspect='auto')
        ax.title.set_text('Pitch Prediction')
        ax.set_xlabel('Time')
        ax.xaxis.set_ticklabels([])  # hide xtick labels
        ax.set_ylabel('Pitch (MIDI number)')
        return ax

    @staticmethod
    def surprisal(ax: matplotlib.axes.Axes, melody_info: MelodyInfo, color=None):
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
    def single_plot(axes_modifier, melody_info, output_path) -> plt.Figure:
        melody_name = melody_info['melody.name'][0]
        fig, ax = plt.subplots()
        axes_modifier(ax=ax, melody_info=melody_info)

        if not os.path.exists(output_path):
            os.makedirs(output_path)
        fig.savefig(fname=output_path + str(melody_name) + '.eps', format='eps', dpi=400)

        return fig

    @staticmethod
    def pianoroll_pitch_distribution_groundtruth(melody_info, output_path) -> plt.Figure:
        melody_name = melody_info['melody.name'][0]
        fig, (ax_distribution, ax_groundtruth) = plt.subplots(1, 2, figsize=(10, 5), dpi=400)
        fig.suptitle('IDyOM Pitch prediction vs ground truth \n\n Melody name: ' + melody_name)

        BasicAxsGeneration.pianoroll_pitch_distribution(ax_distribution, melody_info=melody_info)
        BasicAxsGeneration.pianoroll(ax_groundtruth, melody_info=melody_info)
        ax_groundtruth.title.set_text('Ground Truth')

        plt.tight_layout()

        if not os.path.exists(output_path):
            os.makedirs(output_path)
        fig.savefig(fname=output_path + str(melody_name) + '.eps', format='eps', dpi=400)
        return fig

    @staticmethod
    def pianoroll_surprisal(melody_info, output_path) -> plt.Figure:
        melody_name = melody_info['melody.name'][0]
        fig, (ax_pianoroll, ax_surprisal) = plt.subplots(2, 1, figsize=(8, 5), dpi=400, sharex='col')

        fig.suptitle('Melody: ' + melody_name, fontsize=15)
        BasicAxsGeneration.pianoroll(ax_pianoroll, melody_info=melody_info)
        BasicAxsGeneration.surprisal(ax_surprisal, melody_info=melody_info)

        plt.tight_layout()

        if not os.path.exists(output_path):
            os.makedirs(output_path)
        fig.savefig(fname=output_path + str(melody_name) + '.eps', format='eps', dpi=400)

        return fig


def func():
    dat_path = '/Users/xinyiguan/Codes/IDyOM_Interface_paper/99030821134014-cpitch_onset-cpitch_onset-66030821134014-nil-melody-nil-1-both-nil-t-nil-c-nil-t-t-x-3.dat'
    dataset_info = ExperimentInfo(dat_file_path=dat_path)
    melody = dataset_info.access_melodies()[2]
    output_path = './plots/'
    # fig = BasicPlot.single_plot(axes_modifier= BasicAxsGeneration.surprisal,melody_info=melody,output_path=output_path)
    # fig = BasicPlot.pianoroll_surprisal(melody_info=melody, output_path=output_path)
    fig = BasicPlot.pianoroll_pitch_distribution_groundtruth(melody_info=melody, output_path=output_path)
    fig.show()


if __name__ == '__main__':
    func()
