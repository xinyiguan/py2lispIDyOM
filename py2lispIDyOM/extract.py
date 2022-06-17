import typing
from dataclasses import dataclass
from glob import glob

import numpy as np
import pandas as pd


def to_float(f):
    try:
        return float(f)
    except ValueError:
        return f


def get_dictionary(file: str) -> dict:
    """
    Read the file line by line, split each line into n fields, then create the dictionary:
    :param: file
    :return: dict
    """

    dict = {}
    # f = open(file, "r")
    with open(file, 'r') as f:
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
            dict[fields[1]][key].append(to_float(fields[k]))
            k += 1
    return dict


def get_all_song_dict(dat_file_path: str) -> dict:
    all_song_dict = get_dictionary(dat_file_path)
    return all_song_dict


def get_song_dict_of_interest(all_song_dict, melody_id):
    return list(all_song_dict.values())[melody_id]


def getDataFrame(file: str) -> pd.DataFrame:
    df = pd.read_table(file, delim_whitespace=True)
    return df


class MelodyInfo(pd.DataFrame):
    """
    A melody object (pd.DataFrame) that contains all data in a single melody inherit from the parent Experiment.

    """

    _metadata = ['exp_pitch_element_list', 'parent_experiment']

    def __init__(self, exp_pitch_element_list, parent_experiment, *args, **kw):
        super().__init__(*args, **kw)
        self.exp_pitch_element_list = exp_pitch_element_list
        self.parent_experiment = parent_experiment
        self.melody_name_pp = self._get_melody_name_pprint()

    def access_idyom_output_keywords(self, output_keywords: typing.List[str]):
        """
        Access certain idyom output(s) via its (their) keyword(s).

        :param output_keywords: A list of IDyOM output keywords (e.g., ['cpitch.information.content', 'onset', 'entropy'])
        :type output_keywords: typing.List[str]

        :return: a dataframe containing all data of the selected IDyOM outputs according to the specified keywords.
        :rtype: pd.DataFrame
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

    def get_idyom_output_nparray(self, idyom_output_key: str):
        """
        Get the IDyOM output via its key as a np.array

        :param idyom_output_key: list of str
        :return: an array of the specified output values
        :rtype: np.array
        """

        output_values = self.access_idyom_output_keywords([idyom_output_key]).values.tolist()
        output_values_array = np.array([item for sublist in output_values for item in sublist])
        return output_values_array

    def get_idyom_output_keyword_list(self) -> list:
        """
        Get a list of available IDyOM output keyword for this melody.

        :return: a list of available IDyOM output keyword
        :rtype: list(str)
        """

        idyom_output_keyword_list = self.keys().to_list()
        return idyom_output_keyword_list

    def compute_properties_means(self, idyom_outputs: typing.List[str]):
        """
        Compute the mean values of the idyom outputs.

        :param idyom_outputs: list of idyom output keyword to compute the means
        :type: typing.List[str]

        :return: the mean values of selected idyom outputs
        :rtype: DataFrame
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

    def _get_onset_beat_nparray(self):
        onset_values = np.int_(self.access_idyom_output_keywords(['onset']).values.tolist())
        onset_in_beat = onset_values / 24
        onset_in_beat_array = [item for sublist in onset_in_beat for item in sublist]
        return onset_in_beat_array

    def _get_melody_name_pprint(self) -> str:
        melody_name_pprint = str(self.access_idyom_output_keywords(['melody.name']).to_numpy()[0][0]).replace('"', '')
        return melody_name_pprint

    def _get_pianoroll_pitch_distribution(self):
        pitch_range = (np.amin(self.exp_pitch_element_list), np.amax(self.exp_pitch_element_list))
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
        pitch_range = (np.amin(self.exp_pitch_element_list), np.amax(self.exp_pitch_element_list))
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

    :param experiment_folder_path: the path to experiment log folder which you want to access.
    :type experiment_folder_path: str
    """

    experiment_folder_path: str

    def __post_init__(self):
        self.dat_file_path = sorted(glob(self.experiment_folder_path + 'experiment_output_data_folder/*'))[0]
        self.df = pd.read_table(self.dat_file_path, delim_whitespace=True)
        self.exp_pitch_element_list = self._get_datasetwise_cpitch_elements()
        self.melodies_dict = self.melody_dictionary()

    def melody_dictionary(self) -> typing.Dict[str, MelodyInfo]:
        """
        Get a dictionary of all melodies in the experiment with melody name as the key and all melody info as the value.

        :return: a dictionary consisting of:

                 - melody_name: the name of the melody
                 - MelodyInfo: a MelodyInfo class containing all IDyOM output data of the melody


        :rtype: typed dict -> {melody_name: MelodyInfo}
        """

        return_dict = {}
        my_dict = get_dictionary(self.dat_file_path)
        for key, value in my_dict.items():
            melody_info = MelodyInfo(data=value, parent_experiment=self,
                                     exp_pitch_element_list=self._get_datasetwise_cpitch_elements())
            melody_name = melody_info['melody.name'][0]
            return_dict[melody_name] = melody_info
        return return_dict

    def access_melodies(self, starting_index=None, ending_index=None,
                        melody_names=None):
        """
        Access specific melodies by index or melody names.
        If all arguments are None, then the default is to access all melodies in the Experiment class

        :param starting_index: the index of the melody you want to start accessing
        :type starting_index: int

        :param ending_index: the index of the melody you want to end accessing
        :type ending_index: int

        :param melody_names: list of meldoy names you want to access
        :type melody_names: list(str)

        :return: a list of MelodyInfo class objects (selected melodies)
        :rtype: list(MelodyInfo)
        """

        if melody_names is not None:
            selected_melodies = list(map(self.melodies_dict.get, melody_names))
        else:
            selected_melodies = list(self.melodies_dict.values())[starting_index:ending_index]

        return selected_melodies

    def _get_datasetwise_cpitch_elements(self):
        """
        Get the list of cpitch (full cpitch distribution elements used in IDyOM)

        :return:  a list of int
        """
        # find the cpitches in idyom output keys such as 'cpitch.

        df_all_keys = self.df.keys().to_list()
        cpitch_keys = [keyword for keyword in df_all_keys if 'cpitch' in keyword]
        cpitch_num_keys = [item for item in cpitch_keys if any([char.isdigit() for char in item])]
        pitch_element_list = [item.replace('cpitch.', '') for item in cpitch_num_keys]
        pitch_element_list = np.int_(pitch_element_list)

        return pitch_element_list
