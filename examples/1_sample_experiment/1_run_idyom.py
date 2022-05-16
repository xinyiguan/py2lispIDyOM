"""
This is a sample script to show how to configure and run the IDyOM model.

For more detailed descriptions of the "run IDyOM" functionality, see the 'tutorials/runIDyOM_tutorial.md'
"""

from modules.run import IDyOMExperiment


def my_idyom_experiment():
    # 1. Set experiment configuration:

    my_experiment = IDyOMExperiment(test_dataset_path='dataset/bach_dataset/',
                                    pretrain_dataset_path='dataset/shanx_dataset/',
                                    experiment_history_folder_path='')

    # 2. Set model parameters:

    my_experiment.set_parameters(target_viewpoints=['cpitch', 'onset'],
                                 source_viewpoints=['cpitch', 'onset'],
                                 models=':both',
                                 k=1,
                                 detail=3)

    # 3. Run IDyOM model:

    my_experiment.run()


if __name__ == '__main__':
    my_idyom_experiment()
