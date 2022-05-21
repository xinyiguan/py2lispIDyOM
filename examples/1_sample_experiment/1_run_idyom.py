"""
This is a sample script to show how to configure and run the IDyOM model.

In this example,

- We will have the model pretrain on a chinese corpus ('shanx_dataset/') and test the model on the european corpus ('bach_dataset/').

- The viewpoints to predict (target viewpoint) and the viewpoints to use in prediction (source viewpoint) are both cpitch and onset.

- We will use the ':both' model, and we don't want resampling (i.e., k=1).

For more detailed descriptions of the "run IDyOM" functionality, see the 'tutorial/runIDyOM_tutorial.md'
"""

from py2lispIDyOM.run import IDyOMExperiment


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
