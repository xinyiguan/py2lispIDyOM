import os
from dataclasses import field, dataclass
import configuration as configuration


@dataclass
class IDyOMExperiment:
    train_dataset_path: str
    test_dataset_path: str
    experiment_history_folder_path: str = None

    required_parameters: configuration.RequiredParameters = field(default_factory=configuration.RequiredParameters)
    statistical_modelling_parameters: configuration.StatisticalModellingParameters = field(
        default_factory=configuration.StatisticalModellingParameters)
    training_parameters: configuration.TrainingParameters = field(default_factory=configuration.TrainingParameters)
    viewpoint_selection_parameters: configuration.ViewpointSelectionParameters = field(
        default_factory=configuration.ViewpointSelectionParameters)
    output_parameters: configuration.OutputParameters = field(default_factory=configuration.OutputParameters)
    caching_parameters: configuration.CachingParameters = field(default_factory=configuration.CachingParameters)

    def __post_init__(self):
        self.this_exp_logger = configuration.ExperimentLogger(train_dataset_path=self.train_dataset_path,
                                                              test_dataset_path=self.test_dataset_path,
                                                              experiment_history_folder_path=self.experiment_history_folder_path)
        self.this_experiment_folder_path = self.this_exp_logger.this_exp_folder
        self.test_dataset_exp_folder = self.this_exp_logger.test_dataset_exp_folder
        self.train_dataset_exp_folder = self.this_exp_logger.train_dataset_exp_folder

        self.idyom_config = configuration.IDyOMConfiguration(required_parameters=self.required_parameters,
                                                             statistical_modelling_parameters=self.statistical_modelling_parameters,
                                                             training_parameters=self.training_parameters,
                                                             viewpoint_selection_parameters=self.viewpoint_selection_parameters,
                                                             output_parameters=self.output_parameters,
                                                             caching_parameters=self.caching_parameters,
                                                             this_exp_log_path=self.this_experiment_folder_path)

    def run_start_idyom(self):
        self.idyom_config.run_start_idyom_command()

    def run_import_datasets(self):
        command = self.idyom_config.import_datasets_command()
        os.system(command)

    def run_describe_database(self):
        self.idyom_config.describe_database_command()

    def run_describe_database_detail(self):
        self.idyom_config.describe_detailed_database_command()

    def generate_lisp_script(self):
        self.idyom_config.generate_lisp_script()

    def run_quit(self):
        self.idyom_config.quit_command()

    def run(self):
        self.idyom_config.generate_lisp_script()
        self.idyom_config.run()


def new_test():
    pretraining_dataset_path = 'dataset/bach_dataset/'
    test_dataset_path = 'dataset/shanx_dataset/'

    required_parameters = configuration.RequiredParameters(target_viewpoints=['cpitch', 'onset'],
                                                           source_viewpoints=['cpitch', 'onset'])

    training_parameters = configuration.TrainingParameters(k=1)
    statistical_modelling_parameters = configuration.StatisticalModellingParameters(models=':both+')

    output_parameters = configuration.OutputParameters(detail=3)

    my_exp = IDyOMExperiment(train_dataset_path=pretraining_dataset_path,
                             test_dataset_path=test_dataset_path,
                             required_parameters=required_parameters,
                             statistical_modelling_parameters=statistical_modelling_parameters,
                             training_parameters=training_parameters,
                             output_parameters=output_parameters)

    my_exp.run()


if __name__ == '__main__':
    new_test()
