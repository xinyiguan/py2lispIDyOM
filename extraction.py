"""
Created by xinyiguan on 17.03.22.
"""
import os
import typing
from dataclasses import dataclass
from glob import glob

import numpy as np
import pandas as pd


def toFloat(f):
    try:
        return float(f)
    except ValueError:
        return f


def getDictionary(file: str) -> dict:
    """
    read the file line by line, split each line into n fields, then create the dictionary:
    :param: file
    :return: dict
    """
    dict = {}
    f = open(file, "r")
    lines = f.readlines()
    keys = lines[0].split()
    for i in range(1, len(lines)):
        fields = lines[i].split()

        if fields[1] not in dict:
            dict[fields[1]] = {}  # create dict for each melody

        k = 0
        for key in keys:
            if key not in dict[fields[1]]:
                dict[fields[1]][key] = []
            dict[fields[1]][key].append(toFloat(fields[k]))
            k += 1
    return dict


def get_all_song_dict(dat_file_path: str) -> dict:
    all_song_dict = getDictionary(dat_file_path)
    return all_song_dict


def get_song_dict_of_interest(all_song_dict, melody_id):
    return list(all_song_dict.values())[melody_id]


def getDataFrame(file: str) -> pd.DataFrame:
    df = pd.read_table(file, delim_whitespace=True)
    return df


class MelodyInfo(pd.DataFrame):
    _metadata = ['pitch_range', 'parent_experiment']

    def __init__(self, parent_experiment, *args, **kw):
        super().__init__(*args, **kw)
        self.pitch_range = self.get_pitch_range()
        self.parent_experiment = parent_experiment

    def access_properties(self, properties: typing.List[str]):
        return self[properties]

    def access_mean_properties(self, properties: typing.List[str]):
        cropped_df = self[properties]
        return cropped_df.mean(axis=0)

    def get_pitch_range(self, padding: typing.Optional[int] = 0):
        pitches = self.access_properties(['cpitch'])
        max_pitch = int(pitches.max())
        min_pitch = int(pitches.min())
        pitch_range = (min_pitch - padding, max_pitch + padding)
        return pitch_range

    def get_pianoroll_pitch_distribution(self):
        pitch_range = self.parent_experiment.pitch_range
        pitch_distribution = []
        melody_length = len(self.access_properties(['cpitch.probability']))
        for i in range(*pitch_range):
            key_to_look = 'cpitch.' + str(i)
            if key_to_look not in self.keys():
                one_pitch_prob_across_time = [0] * melody_length
            else:
                one_pitch_prob_across_time = self[key_to_look]
            pitch_distribution.append(one_pitch_prob_across_time)
        pitch_distribution = np.array(pitch_distribution)
        durations = self.access_properties((['dur'])).to_numpy(dtype=int).reshape(-1)
        pitch_distribution = np.repeat(pitch_distribution, repeats=durations, axis=1)
        return pitch_distribution

    def get_pianoroll_original(self):
        pitch_range = self.parent_experiment.pitch_range
        piano_roll = np.arange(*pitch_range)
        piano_roll = (piano_roll == self.access_properties(['cpitch']).to_numpy()).T
        durations = self.access_properties((['dur'])).to_numpy(dtype=int).reshape(-1)
        piano_roll = np.repeat(piano_roll, repeats=durations, axis=1)
        return piano_roll

    def get_onset_time_vector(self):
        onset_seq = self.access_properties(['onset'])
        onset_seq_int = np.int_(onset_seq)
        onset_time_vector = np.arange(0, onset_seq_int[-1] + 1)
        return onset_time_vector

    def get_surprisal_array(self):
        # ic_seq = surprisal seq
        onset_seq_int = np.int_(self.access_properties(['onset']))
        onset_time_vector = self.get_onset_time_vector()
        extended_ic_seq = np.zeros(len(onset_time_vector))

        ic_seq = self.access_properties(['information.content'])
        np.put(extended_ic_seq, onset_seq_int, ic_seq)
        return extended_ic_seq


@dataclass
class ExperimentInfo:
    experiment_folder_path: str

    def __post_init__(self):
        self.dat_file_path = sorted(glob(self.experiment_folder_path + 'experiment_output_data_folder/*'))[0]
        self.df = pd.read_table(self.dat_file_path, delim_whitespace=True)
        self.melodies_dict = self.initialize_melody_dict()
        self.pitch_range = self.get_datasetwise_pitch_range()

    def initialize_melody_dict(self) -> typing.Dict[str, MelodyInfo]:
        """
        :return: a typed dictionary (melody_name, MelodyInfo)
        """
        return_dict = {}
        my_dict = getDictionary(self.dat_file_path)
        for key, value in my_dict.items():
            melody_info = MelodyInfo(data=value, parent_experiment=self)
            melody_name = melody_info['melody.name'][0]
            return_dict[melody_name] = melody_info
        return return_dict

    def access_melodies(self, starting_index=None, ending_index=None,
                        melody_names=None):
        """
        if all arguments are None => default is to access all melodies in the Experiment class
        :param starting_index:
        :param ending_index:
        :param melody_names:
        :return: a list of MelodyInfo class objects (selected melodies)
        """
        if melody_names is not None:
            selected_melodies = list(map(self.melodies_dict.get, melody_names))
        else:
            selected_melodies = list(self.melodies_dict.values())[starting_index:ending_index]

        return selected_melodies

    def get_datasetwise_pitch_range(self):
        pitches = self.df['cpitch']
        pitch_range = (int(pitches.min()), int(pitches.max()))
        return pitch_range


def func():
    dataset_pitchrange = ExperimentInfo(
        experiment_folder_path='experiment_history/04-05-22_14.35.26/').get_datasetwise_pitch_range()

    # melody1 = dataset_info.access_melodies(melody_names=['"shanx002"'])[0]

    print(dataset_pitchrange)


if __name__ == '__main__':
    func()
