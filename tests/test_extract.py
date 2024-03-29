"""
This test script concerns the extract functionality.
We will use the IDyOM outputs from the experiment "25-05-22_14.10.29"
"""
import numpy as np
from unittest import TestCase

import pandas as pd

from py2lispIDyOM.extract import MelodyInfo, ExperimentInfo
from py2lispIDyOM.extract import get_song_dict_of_interest, get_all_song_dict


class TestExtract(TestCase):
    experiment_folder_path = './tests/experiment_history/25-05-22_14.10.29/'

    def test_experimentinfo_extract(self):
        experiment_folder_path = self.experiment_folder_path

        my_exp = ExperimentInfo(experiment_folder_path=experiment_folder_path)
        all_melodies = my_exp.access_melodies()
        self.assertEqual(len(all_melodies), 15)
        for i in range(len(all_melodies)):
            self.assertIsInstance(obj=all_melodies[i], cls=MelodyInfo)

    def test_melodyinfo_extract(self):
        experiment_folder_path = self.experiment_folder_path
        my_exp = ExperimentInfo(experiment_folder_path=experiment_folder_path)
        test_melody = my_exp.access_melodies(melody_names=['"chor-005"'])[0]

        all_song_dict = get_all_song_dict(
            dat_file_path=experiment_folder_path + 'experiment_output_data_folder/66052522141029-cpitch_onset-cpitch_onset-99052522141029-nil-melody-nil-full-both-8-t-nil-c-nil-t-t-x-3.dat')
        song_dict_of_interest = get_song_dict_of_interest(all_song_dict, melody_id=5)

        keywords_to_match = ['cpitch', 'onset', 'information.content', 'probability', 'entropy']

        for idx, val in enumerate(keywords_to_match):
            self.assertIn(val, test_melody.get_idyom_output_keyword_list())
            self.assertEqual(test_melody.get_idyom_output_nparray(val).all(),
                             np.array(song_dict_of_interest[val]).all())

    def test_raise_error(self):
        # supposed to raise TypeError (extract-85)
        with self.assertRaises(TypeError):
            experiment_folder_path = self.experiment_folder_path
            my_exp = ExperimentInfo(experiment_folder_path=experiment_folder_path)
            my_exp.melodies_dict['"chor-003"'].access_idyom_output_keywords(output_keywords='onset')

        with self.assertRaises(KeyError):
            # supposed to raise KeyError (extract-92)
            experiment_folder_path = self.experiment_folder_path
            my_exp = ExperimentInfo(experiment_folder_path=experiment_folder_path)
            my_exp.melodies_dict['"chor-003"'].access_idyom_output_keywords(output_keywords=['pitch'])

    def test_compute_properties_means(self):
        experiment_folder_path = self.experiment_folder_path
        my_exp = ExperimentInfo(experiment_folder_path=experiment_folder_path)
        melody = my_exp.melodies_dict['"chor-001"']
        result1 = melody.compute_properties_means(idyom_outputs=['entropy'])
        result2 = melody.compute_properties_means(idyom_outputs=['information.content'])
        self.assertIs(type(result1), pd.Series)
        self.assertIs(type(result2), pd.Series)

    def test_get_onset_time_in_seconds(self):
        experiment_folder_path = self.experiment_folder_path
        my_exp = ExperimentInfo(experiment_folder_path=experiment_folder_path)
        melody = my_exp.melodies_dict['"chor-001"']
        result = melody._get_onset_time_in_seconds()
        self.assertIs(type(result), np.ndarray)
        self.assertEqual(result.shape, (39, 1))

    def test_get_pianoroll_pitch_distribution(self):
        experiment_folder_path = self.experiment_folder_path
        my_exp = ExperimentInfo(experiment_folder_path=experiment_folder_path)
        melody = my_exp.melodies_dict['"chor-001"']
        result = melody._get_pianoroll_pitch_distribution()
        self.assertIs(type(result), np.ndarray)
        self.assertEqual(result.shape, (33, 960))

    def test_get_pianoroll_original(self):
        experiment_folder_path = self.experiment_folder_path
        my_exp = ExperimentInfo(experiment_folder_path=experiment_folder_path)
        melody = my_exp.melodies_dict['"chor-001"']
        result = melody._get_pianoroll_original()
        self.assertIs(type(result), np.ndarray)
        self.assertEqual(result.shape, (33, 960))

    def test_get_onset_time_vector(self):
        experiment_folder_path = self.experiment_folder_path
        my_exp = ExperimentInfo(experiment_folder_path=experiment_folder_path)
        melody = my_exp.melodies_dict['"chor-001"']
        result = melody._get_onset_time_vector()
        self.assertIs(type(result), np.ndarray)
        self.assertEqual(result.shape, (889,))

    def test_get_surprisal_array(self):
        experiment_folder_path = self.experiment_folder_path
        my_exp = ExperimentInfo(experiment_folder_path=experiment_folder_path)
        melody = my_exp.melodies_dict['"chor-001"']
        result = melody._get_surprisal_array()
        self.assertIs(type(result), np.ndarray)
        self.assertEqual(result.shape, (889,))