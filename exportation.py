import os
from dataclasses import dataclass
from glob import glob
from typing import List

import numpy as np
import scipy.io

import extraction
from extraction import getDictionary, ExperimentInfo, MelodyInfo


@dataclass
class Exportation:
    experiment_folder_path: str
    features_to_export: List = None  # for available data to export, see SingleViewpoint: ['cpitch', 'onset', 'melody']

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

    def _export(self, export_files_path):
        for i, feature in enumerate(self.features_to_export):
            feature_name = self.features_to_export[i]
            scipy.io.savemat(export_files_path + feature_name + '.mat', mdict={feature_name: np.array(feature)})
        print('Exported data to ' + export_files_path + '!')

    def generate_idyom_output_export_folder(self, export_folder_name):
        idyom_output_export_folder_path = self.experiment_folder_path + export_folder_name + '/'
        if not os.path.exists(idyom_output_export_folder_path):
            os.makedirs(idyom_output_export_folder_path)
        return idyom_output_export_folder_path

    def output2mat(self, melody_names=None):
        """
        By default, this function will export the pre-set data properties of all melodies.
        Users can also specify specific melody by passing the melody name to the melody_name param.
        """
        export_folder_path = self.generate_idyom_output_export_folder(export_folder_name='outputs_in_mat')
        if self.features_to_export is not None:  # user provided what features to export, we export these chosen ones.
            if melody_names is not None:  # user provided specific songs to export, we export these chosen ones.
                for i, melody in enumerate(melody_names):
                    this_melody = self.melodies_info_dict[melody]
                    feature_name = self.features_to_export[i]
                    feature = this_melody.access_properties([feature_name])
                    scipy.io.savemat(export_folder_path + melody + '_' + feature_name + '.mat',
                                     mdict={feature_name: np.array(feature)})

            else:  # no specific songs provided, we export the chosen features for all songs.
                all_song_dict = self.all_song_dict



def test():
    mels_info = Exportation(experiment_folder_path='experiment_history/04-05-22_14.35.26/').melodies_info_dict

    one_song = mels_info['"shanx002"']  # this is a pd.df

    melody_names = mels_info.keys()
    melody_info = mels_info.values()

    # print(one_song.access_properties(['onset']))

    # print(type(one_song))

    mydict = one_song.to_dict()
    print(mydict)


if __name__ == '__main__':
    # Exportation(experiment_folder_path='experiment_history/04-05-22_14.35.26/', data_to_export=['onset']).output2mat(
    #     melody_names=['"shanx002"'])

    test()
