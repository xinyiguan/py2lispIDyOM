"""
This test script concerns the export functionality.
We will use the IDyOM outputs from the experiment "25-05-22_14.10.29"
"""

import unittest
from unittest import TestCase
from py2lispIDyOM.export import Export
from py2lispIDyOM.extract import ExperimentInfo
import numpy as np
import scipy.io
import pandas as pd


class TestExport(TestCase):

    def test_export_mat_files(self):
        experiment_folder_path = '../tests/experiment_history/25-05-22_14.10.29/'
        idyom_output_keywords = ['cpitch', 'onset', 'information.content', 'cpitch.entropy']
        Export(experiment_folder_path=experiment_folder_path,
               idyom_output_keywords=idyom_output_keywords,
               melody_names=['"chor-001"', '"chor-002"']).export2mat()

    def test_export_csv_files(self):
        experiment_folder_path = '../tests/experiment_history/25-05-22_14.10.29/'
        Export(experiment_folder_path=experiment_folder_path,
               melody_names=['"chor-003"', '"chor-004"']).export2csv()

    def test_mat_file_check(self):
        experiment_folder_path = '../tests/experiment_history/25-05-22_14.10.29/'

        chor001 = ExperimentInfo(experiment_folder_path=experiment_folder_path).melodies_dict['"chor-001"']

        chor001_cpitch_mat = scipy.io.loadmat(experiment_folder_path + 'outputs_in_mat/chor001_cpitch.mat')
        chor001_cpitch_mat_data = chor001_cpitch_mat['cpitch']
        chor001_cpitch_mat_data = np.array([x for xs in chor001_cpitch_mat_data for x in xs])

        self.assertEqual(chor001.get_idyom_output_nparray('cpitch').all(), chor001_cpitch_mat_data.all())

        chor001_cpitch_entropy_mat = scipy.io.loadmat(
            experiment_folder_path + 'outputs_in_mat/chor001_cpitch_entropy.mat')
        chor001_cpitch_entropy_mat_data = chor001_cpitch_entropy_mat['cpitch_entropy']
        chor001_cpitch_entropy_mat_data = np.array([x for xs in chor001_cpitch_entropy_mat_data for x in xs])

        self.assertEqual(chor001.get_idyom_output_nparray('cpitch.entropy').all(),
                         chor001_cpitch_entropy_mat_data.all())

        chor001_information_content_mat = scipy.io.loadmat(
            experiment_folder_path + 'outputs_in_mat/chor001_information_content.mat')
        chor001_information_content_mat_data = chor001_information_content_mat['information_content']
        chor001_information_content_mat_data = np.array([x for xs in chor001_information_content_mat_data for x in xs])

        self.assertEqual(chor001.get_idyom_output_nparray('information.content').all(),
                         chor001_information_content_mat_data.all())

        chor001_onset_mat = scipy.io.loadmat(experiment_folder_path + 'outputs_in_mat/chor001_onset.mat')
        chor001_onset_mat_data = chor001_onset_mat['onset']
        chor001_onset_mat_data = np.array([x for xs in chor001_onset_mat_data for x in xs])

        self.assertEqual(chor001.get_idyom_output_nparray('onset').all(), chor001_onset_mat_data.all())

        chor002 = ExperimentInfo(experiment_folder_path=experiment_folder_path).melodies_dict['"chor-002"']

        chor002_cpitch_mat = scipy.io.loadmat(experiment_folder_path + 'outputs_in_mat/chor002_cpitch.mat')
        chor002_cpitch_mat_data = chor002_cpitch_mat['cpitch']
        chor002_cpitch_mat_data = np.array([x for xs in chor002_cpitch_mat_data for x in xs])

        self.assertEqual(chor002.get_idyom_output_nparray('cpitch').all(), chor002_cpitch_mat_data.all())

        chor002_cpitch_entropy_mat = scipy.io.loadmat(
            experiment_folder_path + 'outputs_in_mat/chor002_cpitch_entropy.mat')
        chor002_cpitch_entropy_mat_data = chor002_cpitch_entropy_mat['cpitch_entropy']
        chor002_cpitch_entropy_mat_data = np.array([x for xs in chor002_cpitch_entropy_mat_data for x in xs])

        self.assertEqual(chor002.get_idyom_output_nparray('cpitch.entropy').all(),
                         chor002_cpitch_entropy_mat_data.all())

        chor002_information_content_mat = scipy.io.loadmat(
            experiment_folder_path + 'outputs_in_mat/chor002_information_content.mat')
        chor002_information_content_mat_data = chor002_information_content_mat['information_content']
        chor002_information_content_mat_data = np.array([x for xs in chor002_information_content_mat_data for x in xs])

        self.assertEqual(chor002.get_idyom_output_nparray('information.content').all(),
                         chor002_information_content_mat_data.all())

        chor002_onset_mat = scipy.io.loadmat(experiment_folder_path + 'outputs_in_mat/chor002_onset.mat')
        chor002_onset_mat_data = chor002_onset_mat['onset']
        chor002_onset_mat_data = np.array([x for xs in chor002_onset_mat_data for x in xs])

        self.assertEqual(chor002.get_idyom_output_nparray('onset').all(), chor002_onset_mat_data.all())

    def test_csv_file_check(self):
        experiment_folder_path = '../tests/experiment_history/25-05-22_14.10.29/'

        idyom_keywords_checklist = ['cpitch', 'onset',
                                    'information.content', 'entropy', 'probability']

        chor003 = ExperimentInfo(experiment_folder_path=experiment_folder_path).melodies_dict['"chor-003"']
        chor003_df = pd.read_csv(experiment_folder_path+'outputs_in_csv/chor-003.csv', sep=',')

        for idx, val in enumerate(idyom_keywords_checklist):
            self.assertEqual(chor003[val].all(), chor003_df[val].all())

        chor004 = ExperimentInfo(experiment_folder_path=experiment_folder_path).melodies_dict['"chor-004"']
        chor004_df = pd.read_csv(experiment_folder_path+'outputs_in_csv/chor-004.csv', sep=',')

        for idx, val in enumerate(idyom_keywords_checklist):
            self.assertEqual(chor004[val].all(), chor004_df[val].all())


if __name__ == '__main__':
    unittest.main()
