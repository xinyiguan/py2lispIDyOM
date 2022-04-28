"""
Created by xinyiguan on 28.04.22.
"""

import configuration
import run_idyom

required_parameters = configuration.RequiredParameters(dataset_path='dataset/bach_dataset',
                                                       target_viewpoints=['cpitch', 'onset'],
                                                       source_viewpoints=['cpitch', 'onset',
                                                                          ('cpitch', 'articulation')])
myconfiguration = configuration.Configuration(required_parameters=required_parameters)


def func():
    run_idyom.initialize_experiment_folder(experiment_history_folder='new_exp_his')


if __name__ == '__main__':
    func()
