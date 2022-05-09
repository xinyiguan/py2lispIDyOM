"""
Tasks:
    train and test on bach_chorales
    viewpoints: cpitch, onset
    model: ltm
    cross eval leave-one-out -> k :full
    output: surprisal and entropy

"""
from run import IDyOMExperiment

def bach_chorales_idyom():
    test_dataset_path = 'dataset/bach_chorales/'
    target_viewpoints = ['cpitch', 'onset']
    source_viewpoints = ['cpitch', 'onset']

    my_exp = IDyOMExperiment(test_dataset_path=test_dataset_path)
    my_exp.idyom_config.run_model_configuration.required_parameters.target_viewpoints = target_viewpoints
    my_exp.idyom_config.run_model_configuration.required_parameters.source_viewpoints = source_viewpoints
    my_exp.idyom_config.run_model_configuration.statistical_modelling_parameters.models = ':ltm'
    my_exp.idyom_config.run_model_configuration.training_parameters.k = ':full'

    my_exp.update_idyom_config()

    my_exp.run()


if __name__ == '__main__':
    bach_chorales_idyom()