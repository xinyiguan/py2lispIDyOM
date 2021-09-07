"""
This script is to output the data in .mat format.
"""

import os
import scipy.io
import numpy as np
from helper_scripts import data_extractor
from glob import glob

def song_wise_extraction(song_dict,extraction_methods):
    single_song_data = []
    for extraction in extraction_methods:
        feature = extraction(song_dict).tolist()
        single_song_data.append(feature)
    #single_song_data = np.array(single_song_data,dtype=object)
    return single_song_data

def dataset_wise_extraction(all_song_dict,extraction_methods):
    all_song_data = []
    for index,song_dict in all_song_dict.items():
        single_song_data = song_wise_extraction(song_dict,extraction_methods)
        all_song_data.append(single_song_data)
    all_song_data = np.array(all_song_data,dtype=object)
    return all_song_data

## For more methods, see available ones in the data_extractor.py file

features_method_name_dict = {
    'melody_name': data_extractor.get_melody_name_from_song_dict,
    'cpitch': data_extractor.get_pitch_from_song_dict,
    'onset': data_extractor.get_onset_from_song_dict,
    'overall_probability': data_extractor.get_overall_prob_from_song_dict,
    'overall_information_content': data_extractor.get_overall_information_content_from_song_dict,
    'overall_entropy': data_extractor.get_overall_entropy_from_song_dict,
    'cpitch_information_content': data_extractor.get_cpitch_information_content_from_song_dict,
    'cpitch_entropy': data_extractor.get_cpitch_entropy_from_song_dict,
    'onset_information_content': data_extractor.get_onset_information_content_from_song_dict,
    'onset_entropy': data_extractor.get_onset_entropy_from_song_dict,
}

dict_access_keys = lambda dic,l:[dic[x] for x in l]



def export(data_to_export,output_path):
    for i,feature in enumerate(data_to_export):
        feature_name = list(features_method_name_dict.keys())[i]
        scipy.io.savemat(output_path+feature_name+'.mat', mdict={feature_name: np.array(feature)})
    print('Exported data to '+output_path + '!')



## If run this module only:

def export_mat_from_history_folder(selected_experiment_history_folder, data_type_to_export):
    dat_file_path = sorted(glob(selected_experiment_history_folder + 'experiment_output_data_folder/*'))[0]
    all_song_dict = data_extractor.get_all_song_dict_from_dat(dat_file_path)

    # export data:
    data_to_export = dataset_wise_extraction(all_song_dict,
                                             dict_access_keys(features_method_name_dict, data_type_to_export)).T
    mat_data_output_folder = selected_experiment_history_folder + 'mat_data_outputs/'
    if not os.path.exists(mat_data_output_folder):
        os.makedirs(mat_data_output_folder)
    export(data_to_export,output_path=mat_data_output_folder)


# Pass your desired 'selected_experiment_history_folder' below:
if __name__ == '__main__':
    selected_experiment_history_folder = '/Users/guan/Desktop/Codes/IDyOM_Python_Interface/experiment_history/07-26-21_17.32.52/'
    data_type_to_export = [
        'melody_name',
        'cpitch',
        'onset',
        'overall_probability',
        'overall_information_content',
        'overall_entropy',
        'cpitch_information_content',
        'cpitch_entropy',
        'onset_information_content',
        'onset_entropy',
    ]
    export_mat_from_history_folder(selected_experiment_history_folder, data_type_to_export)
