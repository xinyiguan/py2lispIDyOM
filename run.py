import os
from dataclasses import field, dataclass
import configuration as configuration


@dataclass
class IDyOMExperiment:
    test_dataset_path: str
    pretrain_dataset_path: str = None
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
        self.test_dataset_id = self.generate_test_dataset_id()
        self.pretrain_dataset_id = self.generate_train_dataset_id()

        self.this_exp_logger = configuration.ExperimentLogger(pretrain_dataset_path=self.pretrain_dataset_path,
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

                                                             this_exp_log_path=self.this_experiment_folder_path,
                                                             test_dataset_path=self.test_dataset_path,
                                                             pretrain_dataset_path=self.pretrain_dataset_path,
                                                             test_dataset_id=self.test_dataset_id,
                                                             pretrain_dataset_id=self.pretrain_dataset_id
                                                             )

    def generate_test_dataset_id(self):
        if self.test_dataset_path:
            moment = configuration.get_timestamp()
            dataset_id = '66' + moment
            return dataset_id
        else:
            raise AssertionError("Missing dataset input!")

    def generate_train_dataset_id(self):
        # only generate an ID if pretrain_dataset_path is not None
        if self.pretrain_dataset_path:
            moment = configuration.get_timestamp()
            dataset_id = '99' + moment
            return dataset_id
        else:
            pass

    def run_start_idyom(self):
        """
        This function runs the Lisp command to start IDyOM in SBCL.
        """
        self.idyom_config.run_start_idyom_command()

    def run_import_datasets(self):
        """
        This function runs the Lisp command to import relevant datasets.
        """
        command = self.idyom_config.import_datasets_command()
        os.system(command)

    def run_describe_database(self):
        """
        This function runs the Lisp command to describe the database.
        """
        self.idyom_config.describe_database_command()

    def run_describe_database_detail(self):
        """
        This function runs the Lisp command to describe the database in details.
        """
        self.idyom_config.describe_detailed_database_command()

    def generate_lisp_script(self):
        """
        This function generate a Lisp script.
        """
        self.idyom_config.generate_lisp_script()

    def run_quit(self):
        """
        This function runs the Lisp command to quit.
        """
        self.idyom_config.quit_command()

    def run(self):
        """
        This function runs the Lisp command to generate a Lisp script and run it.
        """
        self.idyom_config.generate_lisp_script()
        self.idyom_config.run()


def new_test():
    test_dataset_path = 'dataset/shanx_dataset/'

    required_parameters = configuration.RequiredParameters(target_viewpoints=['cpitch', 'onset'],
                                                           source_viewpoints=['cpitch', 'onset'])

    training_parameters = configuration.TrainingParameters(k=':full')
    statistical_modelling_parameters = configuration.StatisticalModellingParameters(models=':ltm')

    output_parameters = configuration.OutputParameters(detail=3)

    my_exp = IDyOMExperiment(
        test_dataset_path=test_dataset_path,
        required_parameters=required_parameters,
        statistical_modelling_parameters=statistical_modelling_parameters,
        training_parameters=training_parameters,
        output_parameters=output_parameters)

    my_exp.generate_lisp_script()


if __name__ == '__main__':
    new_test()
