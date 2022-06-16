"""
This test script concerns the extract functionality.
We will use the IDyOM outputs from the experiment "25-05-22_14.10.29"
"""

import unittest
from unittest import TestCase
from py2lispIDyOM.export import Export
from py2lispIDyOM.extract import ExperimentInfo, MelodyInfo
import numpy as np
import scipy.io
import pandas as pd


def generate_mat_files():
    experiment_folder_path = 'experiment_history/25-05-22_14.10.29/'
    idyom_output_keywords = ['cpitch', 'onset', 'information.content', 'cpitch.entropy']
    Export(experiment_folder_path=experiment_folder_path,
           idyom_output_keywords=idyom_output_keywords,
           melody_names=['"chor-001"', '"chor-002"']).export2mat()

def generate_csv_files():
    experiment_folder_path = 'experiment_history/25-05-22_14.10.29/'
    Export(experiment_folder_path=experiment_folder_path,
           melody_names=['"chor-003"', '"chor-004"']).export2csv()

class TestExport(TestCase):

    def export_mat_file_check(self):
        experiment_folder_path = 'experiment_history/25-05-22_14.10.29/'

        chor001 = ExperimentInfo(experiment_folder_path=experiment_folder_path).melodies_dict['"chor-001"']

        chor001_cpitch_mat = scipy.io.loadmat(experiment_folder_path + 'outputs_in_mat/chor001_cpitch.mat')
        chor001_cpitch_mat_data = chor001_cpitch_mat['cpitch']
        chor001_cpitch_mat_data = np.array([x for xs in chor001_cpitch_mat_data for x in xs])

        self.assertEqual(chor001.get_idyom_output_nparray('cpitch'), chor001_cpitch_mat_data)

        chor001_cpitch_entropy_mat = scipy.io.loadmat(experiment_folder_path + 'outputs_in_mat/chor001_cpitch_entropy.mat')
        chor001_cpitch_entropy_mat_data = chor001_cpitch_entropy_mat['cpitch_entropy']
        chor001_cpitch_entropy_mat_data = np.array([x for xs in chor001_cpitch_entropy_mat_data for x in xs])

        self.assertEqual(chor001.get_idyom_output_nparray('cpitch.entropy'), chor001_cpitch_entropy_mat_data)

        chor001_information_content_mat = scipy.io.loadmat(experiment_folder_path + 'outputs_in_mat/chor001_cpitch.mat')
        chor001_information_content_mat_data = chor001_information_content_mat['information_content']
        chor001_information_content_mat_data = np.array([x for xs in chor001_information_content_mat_data for x in xs])

        self.assertEqual(chor001.get_idyom_output_nparray('information.content'), chor001_information_content_mat_data)

        chor001_onset_mat = scipy.io.loadmat(experiment_folder_path + 'outputs_in_mat/chor001_cpitch.mat')
        chor001_onset_mat_data = chor001_onset_mat['onset']
        chor001_onset_mat_data = np.array([x for xs in chor001_onset_mat_data for x in xs])

        self.assertEqual(chor001.get_idyom_output_nparray('onset'), chor001_onset_mat_data)


        chor002 = ExperimentInfo(experiment_folder_path=experiment_folder_path).melodies_dict['"chor-002"']

        chor002_cpitch_mat = scipy.io.loadmat(experiment_folder_path + 'outputs_in_mat/chor002_cpitch.mat')
        chor002_cpitch_mat_data = chor002_cpitch_mat['cpitch']
        chor002_cpitch_mat_data = np.array([x for xs in chor002_cpitch_mat_data for x in xs])

        self.assertEqual(chor002.get_idyom_output_nparray('cpitch'), chor002_cpitch_mat_data)

        chor002_cpitch_entropy_mat = scipy.io.loadmat(experiment_folder_path + 'outputs_in_mat/chor002_cpitch_entropy.mat')
        chor002_cpitch_entropy_mat_data = chor002_cpitch_entropy_mat['cpitch_entropy']
        chor002_cpitch_entropy_mat_data = np.array([x for xs in chor002_cpitch_entropy_mat_data for x in xs])

        self.assertEqual(chor002.get_idyom_output_nparray('cpitch.entropy'), chor002_cpitch_entropy_mat_data)

        chor002_information_content_mat = scipy.io.loadmat(experiment_folder_path + 'outputs_in_mat/chor002_cpitch.mat')
        chor002_information_content_mat_data = chor002_information_content_mat['information_content']
        chor002_information_content_mat_data = np.array([x for xs in chor002_information_content_mat_data for x in xs])

        self.assertEqual(chor002.get_idyom_output_nparray('information.content'), chor002_information_content_mat_data)

        chor002_onset_mat = scipy.io.loadmat(experiment_folder_path + 'outputs_in_mat/chor002_cpitch.mat')
        chor002_onset_mat_data = chor002_onset_mat['onset']
        chor002_onset_mat_data = np.array([x for xs in chor002_onset_mat_data for x in xs])

        self.assertEqual(chor002.get_idyom_output_nparray('onset'), chor002_onset_mat_data)


    def export_csv_file_check(self):
        experiment_folder_path = 'experiment_history/25-05-22_14.10.29/'

        idyom_keywords_checklist = ['cpitch', 'onset', 'cpitch.information.content', 'onset.information.content',
                                    'information.content', 'entropy', 'probability',
                                    'cpitch.probability', 'onset.probability', 'onset.entropy', 'cpitch.entropy']

        chor003 = ExperimentInfo(experiment_folder_path=experiment_folder_path).melodies_dict['"chor-003"']
        chor003_df = pd.read_csv('experiment_history/25-05-22_14.10.29/outputs_in_csv/chor-003.csv')

        for idx, val in idyom_keywords_checklist:
            self.assertEqual(chor003.get_idyom_output_nparray(val), chor003_df.keys(val))





if __name__ == '__main__':
    # generate_mat_files()
    # generate_csv_files()
    unittest.main()


