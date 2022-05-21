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
    """
    A melody object (pd.DataFrame) that contains all data in a single melody inherit from the parent Experiment.

    Attributes
    ----------
    melody_name_pp: str
        The name of the melody.

    Methods
    -------
    access_idyom_output_keywords()(properties: typing.List[str])
        Access certain properties/idyom outputs via its keyword.

    """

    _metadata = ['pitch_range', 'parent_experiment']

    def __init__(self, parent_experiment, *args, **kw):
        super().__init__(*args, **kw)
        self.pitch_range = self.get_pitch_range()
        self.parent_experiment = parent_experiment
        self.melody_name_pp = self._get_melody_name_pprint()

    def access_idyom_output_keywords(self, output_keywords: typing.List[str]):
        """
        Access certain idyom output(s) via its (their) keyword(s).

        :param output_keywords: list of str
            A list of IDyOM output keywords (e.g., ['cpitch.information.content', 'onset', 'entropy'])
        :return: pd.DataFrame
        """
        if isinstance(output_keywords, list):
            pass
        else:
            raise TypeError(f'Argument \'output_keywords\' should be a list of strings, not {type(output_keywords)}')

        def check_condition(keyword) -> bool:
            if keyword in self.get_idyom_output_keyword_list():
                return True
            else:
                raise KeyError(
                    f'Incorrect keyword: \'{keyword}\'. Please check your spelling. Available IDyOM output keywords for this melody are: {self.get_idyom_output_keyword_list()}')

        for idx, keyword in enumerate(output_keywords):
            if check_condition(keyword):
                return self[output_keywords]

    def get_idyom_output_keyword_list(self) -> list:
        """
        Get a list of available IDyOM output keyword for this melody.
        :return: list
        """
        idyom_output_keyword_list = self.keys().to_list()
        return idyom_output_keyword_list

    def compute_properties_means(self, idyom_outputs: typing.List[str]):
        """
        Compute the mean values of the idyom outputs.

        :param idyom_outputs: list of strings
        :return: DataFrame
        """
        cropped_df = self[idyom_outputs]
        return cropped_df.mean(axis=0)

    def _get_onset_time_in_seconds(self):
        onset_values = np.int_(self.access_idyom_output_keywords(['onset']))
        base_onset_values = onset_values / 24  # idyom uses basic time units, quarter note =24
        tempo = np.int_(self.access_idyom_output_keywords(['tempo']))
        bpm = (60 * 1000000) / tempo
        onset_time_in_sec = (bpm / 60) * base_onset_values
        return onset_time_in_sec

    def _get_melody_name_pprint(self) -> str:
        melody_name_pprint = str(self.access_idyom_output_keywords(['melody.name']).to_numpy()[0][0]).replace('"', '')
        return melody_name_pprint

    def get_pitch_range(self, padding: typing.Optional[int] = 5):
        pitches = self.access_idyom_output_keywords(['cpitch'])
        max_pitch = int(pitches.max())
        min_pitch = int(pitches.min())
        pitch_range = (min_pitch - padding, max_pitch + padding)
        return pitch_range

    def _get_pianoroll_pitch_distribution(self):
        pitch_range = self.parent_experiment.pitch_range
        pitch_distribution = []
        melody_length = len(self.access_idyom_output_keywords(['cpitch.probability']))
        for i in range(*pitch_range):
            key_to_look = 'cpitch.' + str(i)
            if key_to_look not in self.keys():
                one_pitch_prob_across_time = [0] * melody_length
            else:
                one_pitch_prob_across_time = self[key_to_look]
            pitch_distribution.append(one_pitch_prob_across_time)
        pitch_distribution = np.array(pitch_distribution)
        durations = self.access_idyom_output_keywords((['dur'])).to_numpy(dtype=int).reshape(-1)
        pitch_distribution = np.repeat(pitch_distribution, repeats=durations, axis=1)
        return pitch_distribution

    def _get_pianoroll_original(self):
        pitch_range = self.parent_experiment.pitch_range
        piano_roll = np.arange(*pitch_range)
        piano_roll = (piano_roll == self.access_idyom_output_keywords(['cpitch']).to_numpy()).T
        durations = self.access_idyom_output_keywords((['dur'])).to_numpy(dtype=int).reshape(-1)
        piano_roll = np.repeat(piano_roll, repeats=durations, axis=1)
        return piano_roll

    def _get_onset_time_vector(self):
        onset_seq = self.access_idyom_output_keywords(['onset'])
        onset_seq_int = np.int_(onset_seq)
        onset_time_vector = np.arange(0, onset_seq_int[-1] + 1)
        return onset_time_vector

    def _get_surprisal_array(self):
        # ic_seq = surprisal seq
        onset_seq_int = np.int_(self.access_idyom_output_keywords(['onset']))
        onset_time_vector = self._get_onset_time_vector()
        extended_ic_seq = np.zeros(len(onset_time_vector))

        ic_seq = self.access_idyom_output_keywords(['information.content'])
        np.put(extended_ic_seq, onset_seq_int, ic_seq)
        return extended_ic_seq


@dataclass
class ExperimentInfo:
    """
    An experiment object that contains all data in a single experiment.

    Parameters
    ----------
    experiment_folder_path: str
        The path to experiment log folder which you want to access.

    Attributes
    ----------
    melodies_dict: dict
        A typed dictionary (melody_name, MelodyInfo).
    pitch_range: tuple of int
        The pitch range of the entire dataset.

    Methods
    -------
    access_melodies(starting_index=None, ending_index=None,melody_names=None)
        Access specific melodies by index or melody names. If all arguments are None, then the default is to access
        all melodies in the Experiment class.

    """
    experiment_folder_path: str

    def __post_init__(self):
        self.dat_file_path = sorted(glob(self.experiment_folder_path + 'experiment_output_data_folder/*'))[0]
        self.df = pd.read_table(self.dat_file_path, delim_whitespace=True)
        self.melodies_dict = self.melody_dictionary()
        self.pitch_range = self._get_datasetwise_pitch_range()

    def melody_dictionary(self) -> typing.Dict[str, MelodyInfo]:
        """
        Get a dictionary of all melodies in the experiment with melody name as the key and all melody info as the value.

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
        Access specific melodies by index or melody names.
        If all arguments are None, then the default is to access all melodies in the Experiment class

        :param starting_index: int
        :param ending_index: int
        :param melody_names: list of str
        :return: a list of MelodyInfo class objects (selected melodies)
        """
        if melody_names is not None:
            selected_melodies = list(map(self.melodies_dict.get, melody_names))
        else:
            selected_melodies = list(self.melodies_dict.values())[starting_index:ending_index]

        return selected_melodies

    def _get_datasetwise_pitch_range(self):
        """
        Get the pitch range of the entire dataset.
        :return:  a tuple of int
        """
        pitches = self.df['cpitch']
        pitch_range = (int(pitches.min()), int(pitches.max()))
        return pitch_range


if __name__ == '__main__':
    experiment_history_folder = 'experiment_history/04-05-22_14.35.26/'
    my_exp = ExperimentInfo(experiment_history_folder)
    song = my_exp.access_melodies(starting_index=3, ending_index=6)[0]
    print(song)