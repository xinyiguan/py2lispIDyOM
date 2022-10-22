import unittest
from unittest import TestCase, mock
from unittest.mock import MagicMock, patch

import matplotlib.pyplot as plt

from py2lispIDyOM.extract import MelodyInfo, ExperimentInfo
import py2lispIDyOM.viz as viz


class Test(TestCase):
    experiment_folder_path = './tests/experiment_history/25-05-22_14.10.29/'
    # experiment_folder_path = 'experiment_history/25-05-22_14.10.29/'

    my_exp = ExperimentInfo(experiment_folder_path=experiment_folder_path)
    all_melodies = my_exp.access_melodies()

    def test_idyom_output_along_time(self):
        valid_idyom_output_keyword_list = self.my_exp.melodies_dict['"chor-001"'].get_idyom_output_keyword_list()
        ground_truth_output = ['dataset.id', 'melody.id', 'note.id', 'melody.name', 'vertint12', 'articulation',
                               'comma',
                               'voice', 'ornament', 'dyn', 'phrase', 'bioi', 'deltast', 'accidental', 'mpitch',
                               'cpitch',
                               'barlength', 'pulses', 'tempo', 'mode', 'keysig', 'dur', 'onset',
                               'cpitch.order.ltm.cpitch',
                               'cpitch.order.stm.cpitch', 'cpitch.weight.ltm', 'cpitch.weight.stm',
                               'cpitch.weight.ltm.cpitch',
                               'cpitch.weight.stm.cpitch', 'cpitch.probability', 'cpitch.information.content',
                               'cpitch.entropy',
                               'cpitch.55', 'cpitch.57', 'cpitch.58', 'cpitch.59', 'cpitch.60', 'cpitch.62',
                               'cpitch.63',
                               'cpitch.64', 'cpitch.65', 'cpitch.66', 'cpitch.67', 'cpitch.68', 'cpitch.69',
                               'cpitch.70',
                               'cpitch.71', 'cpitch.72', 'cpitch.73', 'cpitch.74', 'cpitch.75', 'cpitch.76',
                               'cpitch.77',
                               'cpitch.78', 'cpitch.79', 'cpitch.81', 'cpitch.82', 'cpitch.83', 'cpitch.84',
                               'cpitch.85',
                               'cpitch.86', 'cpitch.88', 'onset.order.ltm.onset', 'onset.order.stm.onset',
                               'onset.weight.ltm',
                               'onset.weight.stm', 'onset.weight.ltm.onset', 'onset.weight.stm.onset',
                               'onset.probability',
                               'onset.information.content', 'onset.entropy', 'onset.0', 'onset.3', 'onset.6', 'onset.9',
                               'onset.12', 'onset.18', 'onset.24', 'onset.36', 'onset.48', 'onset.72', 'onset.120',
                               'probability', 'information.content', 'entropy', 'information.gain']
        self.assertEqual(ground_truth_output, valid_idyom_output_keyword_list)

    def test_one_ic_along_onsets(self):
        onset_in_beat_len = len(self.my_exp.melodies_dict['"chor-001"']._get_onset_beat_nparray())
        onset_answer_len = 39

        chosen_ic_len = len(self.my_exp.melodies_dict['"chor-001"'].get_idyom_output_nparray(idyom_output_key='information.content'))
        ic_answer_len = 39

        self.assertEqual(onset_in_beat_len, onset_answer_len)
        self.assertEqual(chosen_ic_len,ic_answer_len)

    def test_one_entropy_along_onsets(self):
        onset_in_beat_len = len(self.my_exp.melodies_dict['"chor-003"']._get_onset_beat_nparray())
        onset_answer_len = 34

        chosen_entropy_len = len(self.my_exp.melodies_dict['"chor-003"'].get_idyom_output_nparray(idyom_output_key='entropy'))
        entropy_answer_len = 34

        self.assertEqual(onset_in_beat_len, onset_answer_len)
        self.assertEqual(chosen_entropy_len,entropy_answer_len)

if __name__ == '__main__':
    unittest.main()
