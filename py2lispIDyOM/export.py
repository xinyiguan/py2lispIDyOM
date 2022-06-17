import os
from dataclasses import dataclass
from glob import glob
from typing import List

import numpy as np
import pandas as pd
import scipy.io

from py2lispIDyOM.extract import ExperimentInfo


@dataclass
class Export:
    """Export selected IDyOM model outputs to other formats.

    :param experiment_folder_path: the path to which you saved all the result data/plots
    :type experiment_folder_path: str

    :param idyom_output_keywords: a list of IDyOM output keywords you want to export. To see a full list of valid idyom_output_keywords, use the method: extract.get_idyom_output_keyword_list()
    :type idyom_output_keywords: typing.List[str]

    :param melody_names: a list of melodies of which IDyOM outputs that you want to export
    :type melody_names: list(str)
    """

    experiment_folder_path: str
    idyom_output_keywords: List = None
    melody_names: List = None

    def __post_init__(self):
        self.dat_file_path = glob(self.experiment_folder_path + 'experiment_output_data_folder/*.dat')[0]
        self.experiment_info = ExperimentInfo(experiment_folder_path=self.experiment_folder_path)
        self.melodies_info_dict = self.experiment_info.melodies_dict

    def _generate_export_folder(self, export_folder_name):
        """To generate a folder to store the idyom outputs in other formats (e.g., .mat, .csv)"""
        idyom_output_export_folder_path = self.experiment_folder_path + export_folder_name + '/'
        if not os.path.exists(idyom_output_export_folder_path):
            os.makedirs(idyom_output_export_folder_path)
        return idyom_output_export_folder_path

    def _get_valid_idyom_output_keys(self, melody):
        """To get a list of valid idyom output keys for a melody."""
        valid_idyom_output_keys = self.melodies_info_dict[melody].get_idyom_output_keyword_list()
        return valid_idyom_output_keys

    def _get_idyom_output_for_single_melody(self, melody, idyom_key):
        """To get the IDyOM output value array for a single melody, according to the IDyOM output keys."""
        output_value_array = self.melodies_info_dict[melody].access_idyom_output_keywords(
            [idyom_key]).values  # this is np.array
        output_value_array = output_value_array.flatten()
        return output_value_array

    def _get_single_melody_output_values_df(self, melody):
        """This function returns a DataFrame of all IDyOM output values of one melody."""
        idyom_output_values_df = self.melodies_info_dict[melody]
        return idyom_output_values_df

    def _get_output_values_in_selected_melodies(self, idyom_key, selected_songs):
        """This function returns a np.array of idyom output values for selected an idyom key for each selected songs."""
        output_values_data_in_songs = []
        for index, melody in enumerate(selected_songs):
            valid_keys = self._get_valid_idyom_output_keys(melody=melody)
            if idyom_key in valid_keys:
                idyom_data = self._get_idyom_output_for_single_melody(melody=melody, idyom_key=idyom_key)
                output_values_data_in_songs.append(idyom_data)
            else:
                raise KeyError(
                    f'IDyOM output keyword \'{idyom_key}\' is invalid. Valid IDyOM output keys are: {valid_keys}')
        output_values_data_in_songs = np.array(output_values_data_in_songs, dtype=object)
        return output_values_data_in_songs

    def _get_output_values_df_in_selected_melodies(self, selected_songs):
        """
        This function iterate through the func '_get_single_melody_output_values_df' to get
        a DataFrame of idyom output values for all idyom keys for each selected songs.
         """
        for index, melody in selected_songs:
            self._get_single_melody_output_values_df(melody=melody)

    def _export_by_keyword_2mat(self, keywords_list, selected_songs, output_path):
        """Export the idyom output data to .mat files according to the keyword list."""

        # Type check =====================:
        if isinstance(keywords_list, list):
            pass
        else:
            raise TypeError(f'Argument \'keywords_list\' should be a list of strings, not {type(keywords_list)}')

        for i, keyword in enumerate(keywords_list):  # data_to_export is a list of list
            keyword_output_data_in_songs = self._get_output_values_in_selected_melodies(idyom_key=keyword,
                                                                                        selected_songs=selected_songs)
            keyword_name_pp = keyword.replace('.', '_')  # account for names like "information.content"
            keyword_name_pp = keyword_name_pp.replace('-', '')
            scipy.io.savemat(output_path + keyword_name_pp + '.mat',
                             mdict={keyword_name_pp: np.array(keyword_output_data_in_songs)})
        print('Exported data to ' + output_path)

    def _export_values_of_keywords_by_melody_2mat(self, keywords_list, melody, output_path):
        """Exports the IDyOM output values according to the keywords_list of one song to a mat file."""
        # Type check =====================:
        if isinstance(keywords_list, list):
            pass
        else:
            raise TypeError(f'Argument \'keywords_list\' should be a list of strings, not {type(keywords_list)}')
        melody_name_pp = melody.replace('"', '')
        for i, keyword in enumerate(keywords_list):
            idyom_output_data_in_song = self._get_idyom_output_for_single_melody(melody=melody, idyom_key=keyword)
            idyom_keyword_pp = keyword.replace('.', '_')  # account for names like "information.content"
            full_outfile_name = melody_name_pp + '_' + idyom_keyword_pp
            full_outfile_name = full_outfile_name.replace('-', '')
            scipy.io.savemat(output_path + full_outfile_name + '.mat',
                             mdict={idyom_keyword_pp: np.array(idyom_output_data_in_song)})
        print('Exported data to ' + output_path)

    def _export_by_song_2csv(self, melody_name, single_song_df_data: pd.DataFrame, output_path):
        """Exports the all the IDyOM output data (df) for a single melody to csv"""
        melody_name = melody_name.replace('"', '')
        csv_file_path = output_path + melody_name + '.csv'
        single_song_df_data.to_csv(path_or_buf=csv_file_path, index=False, header=True)

    def export2mat(self):
        """
        This function exports the IDyOM output data to mat files.
        By default, it will export the outputs according to the preset keywords specified in the idyom_output_keywords for all melodies.
        Users can also specify specific melody by passing the melody names to the melody_name param.

        :return (a) mat file(s) containing the selected IDyOM output data

        """
        # Check idyom_output_keyword is not None:
        if self.idyom_output_keywords is None:
            raise ValueError(f'The argument \'idyom_output_keywords\' is empty. '
                             f'Please provide a list of IDyOM output keywords of which you want to export to mat files.')
        else:
            pass
        export_folder_path = self._generate_export_folder(export_folder_name='outputs_in_mat')
        keywords = self.idyom_output_keywords

        if keywords:
            if self.melody_names:
                for index, melody in enumerate(self.melody_names):
                    self._export_values_of_keywords_by_melody_2mat(keywords_list=keywords, melody=melody,
                                                                   output_path=export_folder_path)

            else:
                melody_names = list(self.melodies_info_dict.keys())
                self._export_by_keyword_2mat(keywords_list=keywords, selected_songs=melody_names,
                                             output_path=export_folder_path)

    def export2csv(self):
        """
        This function exports the IDyOM output data to a csv files.
        By default, this will export all properties of the chosen melodies, where each melody is in one csv file.

        :return a csv file containing all IDyOM output data for each selected melody.

        """
        # Check idyom_output_keyword is None:
        if self.idyom_output_keywords is not None:
            raise ValueError(f'The argument \'idyom_output_keywords\' should be empty. '
                             f'The current version of py2lispIDyoM only supports exporting all IDyoM outputs of selected or all melodies.')

        else:
            pass

        export_folder_path = self._generate_export_folder(export_folder_name='outputs_in_csv')

        if self.melody_names:
            for index, melody in enumerate(self.melody_names):
                single_song_df_data = self._get_single_melody_output_values_df(melody=melody)
                self._export_by_song_2csv(melody_name=melody, single_song_df_data=single_song_df_data,
                                          output_path=export_folder_path)

        else:
            melody_names = list(self.melodies_info_dict.keys())
            for index, melody in enumerate(melody_names):
                single_song_df_data = self._get_single_melody_output_values_df(melody=melody)
                self._export_by_song_2csv(melody_name=melody, single_song_df_data=single_song_df_data,
                                          output_path=export_folder_path)

        print('Exported data to ' + export_folder_path)
