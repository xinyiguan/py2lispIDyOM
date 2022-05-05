import os
from dataclasses import dataclass
from glob import glob
from typing import List

import numpy as np
import pandas as pd
import scipy.io

import extraction
from extraction import ExperimentInfo


@dataclass
class Exportation:
    experiment_folder_path: str
    features_to_export: List =None # for available data to export, see SingleViewpoint: ['cpitch', 'onset', 'melody']
    melody_names: List = None

    def __post_init__(self):
        self.dat_file_path = glob(self.experiment_folder_path + 'experiment_output_data_folder/*.dat')[0]
        self.experiment_info = ExperimentInfo(experiment_folder_path=self.experiment_folder_path)
        self.melodies_info_dict = self.experiment_info.melodies_dict
        self.all_song_dict = extraction.get_all_song_dict(dat_file_path=self.dat_file_path)

    def song_wise_extraction(self, song_dict, extraction_methods):
        single_song_data = []
        for extraction in extraction_methods:
            feature = extraction(song_dict).tolist()
            single_song_data.append(feature)
        return single_song_data

    def dataset_wise_extraction(self, extraction_methods):
        all_song_data = []
        for index, song_dict in self.all_song_dict.items():
            single_song_data = self.song_wise_extraction(song_dict, extraction_methods)
            all_song_data.append(single_song_data)
        all_song_data = np.array(all_song_data, dtype=object)
        return all_song_data

    def generate_idyom_output_export_folder(self, export_folder_name):
        idyom_output_export_folder_path = self.experiment_folder_path + export_folder_name + '/'
        if not os.path.exists(idyom_output_export_folder_path):
            os.makedirs(idyom_output_export_folder_path)
        return idyom_output_export_folder_path

    def _get_single_song_feature(self, melody, feature_name):
        feature_array = self.melodies_info_dict[melody].access_properties(feature_name).values  # this is np.array
        return feature_array

    def _get_single_song_features_data_df(self, melody):
        """This function returns a DataFrame of all features values of one song"""
        feature_data_df = self.melodies_info_dict[melody]
        return feature_data_df

    def _get_feature_data_in_selected_songs(self, feature_name, selected_songs):
        """This function returns a np.array of features values for each selected songs."""
        feature_data_in_songs = []
        for index, melody in enumerate(selected_songs):
            feature_data = self._get_single_song_feature(melody=melody, feature_name=feature_name)
            feature_data_in_songs.append(feature_data)
        feature_data_in_songs = np.array(feature_data_in_songs, dtype=object)
        return feature_data_in_songs

    def _get_feature_data_df_in_selected_songs(self, selected_songs):
        for index, melody in selected_songs:
            self._get_single_song_features_data_df(melody=melody)

    def export_by_feature_2mat(self, feature_names_list, selected_songs, output_path):
        for i, feature_name in enumerate(feature_names_list):  # data_to_export is a list of list
            feature_data_in_songs = self._get_feature_data_in_selected_songs(feature_name=feature_name,
                                                                             selected_songs=selected_songs)
            scipy.io.savemat(output_path + feature_name + '.mat', mdict={feature_name: np.array(feature_data_in_songs)})
        print('Exported data to ' + output_path)

    def export_by_song_2csv(self, melody_name, single_song_df_data: pd.DataFrame, output_path):
        melody_name = melody_name.replace('"', '')
        csv_file_path = output_path + melody_name + '.csv'
        single_song_df_data.to_csv(path_or_buf=csv_file_path, index=False, header=True)
        print('Data saved in ' + csv_file_path)

    def export2mat(self):
        """
        By default, this function will export the pre-set data properties of all melodies.
        Users can also specify specific melody by passing the melody names to the melody_name param.
        """
        export_folder_path = self.generate_idyom_output_export_folder(export_folder_name='outputs_in_mat')
        feature_names = self.features_to_export

        if feature_names:
            if self.melody_names:
                self.export_by_feature_2mat(feature_names_list=feature_names, selected_songs=self.melody_names,
                                            output_path=export_folder_path)

            else:
                melody_names = list(self.melodies_info_dict.keys())
                self.export_by_feature_2mat(feature_names_list=feature_names, selected_songs=melody_names,
                                            output_path=export_folder_path)


    def export2csv(self):
        "By default, this will export all features of the chosen melodies, where each melody is in one csv file."
        export_folder_path = self.generate_idyom_output_export_folder(export_folder_name='outputs_in_csv')

        if self.melody_names:
            for index, melody in enumerate(self.melody_names):
                single_song_df_data = self._get_single_song_features_data_df(melody=melody)
                self.export_by_song_2csv(melody_name=melody, single_song_df_data=single_song_df_data,
                                         output_path=export_folder_path)

        else:
            melody_names = list(self.melodies_info_dict.keys())
            for index, melody in enumerate(melody_names):
                single_song_df_data = self._get_single_song_features_data_df(melody=melody)
                self.export_by_song_2csv(melody_name=melody, single_song_df_data=single_song_df_data,
                                         output_path=export_folder_path)



if __name__ == '__main__':

    Exportation(experiment_folder_path='experiment_history/04-05-22_14.35.26/',
                features_to_export=['onset', 'cpitch', 'melody_name'], melody_names=['"shanx002"','"shanx008"']).export2csv()
