import os
from dataclasses import field, dataclass

from configuration import get_timestamp, IDyOMConfiguration, ExperimentLogger


@dataclass
class IDyOMExperiment:
    test_dataset_path: str
    pretrain_dataset_path: str = None
    experiment_history_folder_path: str = None
    idyom_config: IDyOMConfiguration = field(default_factory=IDyOMConfiguration)

    def __post_init__(self):
        self.logger = ExperimentLogger(pretrain_dataset_path=self.pretrain_dataset_path,
                                       test_dataset_path=self.test_dataset_path,
                                       experiment_history_folder_path=self.experiment_history_folder_path)

    def update_idyom_config(self):
        test_dataset_id = self.generate_test_dataset_id()
        train_dataset_id = self.generate_train_dataset_id()
        self.idyom_config.run_model_configuration.required_parameters.dataset_id = test_dataset_id
        self.idyom_config.run_model_configuration.training_parameters.pretraining_id = train_dataset_id

        self.idyom_config.database_configuration.this_exp_log_path = self.logger.this_exp_folder
        self.idyom_config.database_configuration.test_dataset_id = test_dataset_id
        self.idyom_config.database_configuration.pretrain_dataset_id = train_dataset_id
        self.idyom_config.run_model_configuration.output_parameters.output_path = self.logger.output_data_exp_folder

    @staticmethod
    def generate_test_dataset_id() -> str:
        moment = get_timestamp()
        dataset_id = '66' + moment
        return dataset_id

    def generate_train_dataset_id(self):
        # only generate an ID if pretrain_dataset_path is not None
        if self.pretrain_dataset_path:
            moment = get_timestamp()
            dataset_id = '99' + moment
            return dataset_id
        else:
            pass

    def run_start_idyom(self):
        """
        This function runs the Lisp command to start IDyOM in SBCL.
        """
        command = self.idyom_config.start_idyom_command()
        os.system(command)

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

    def run_quit(self):
        """
        This function runs the Lisp command to quit.
        """
        self.idyom_config.quit_command()

    def generate_lisp_script(self):
        path_to_file = self.logger.this_exp_folder
        lisp_file_path = path_to_file + 'compute.lisp'
        lisp_command = self.idyom_config.to_lisp_command()
        with open(lisp_file_path, "w") as f:
            f.write(lisp_command)
        return str(lisp_file_path)

    def run(self):
        """
        This function runs the Lisp command to generate a Lisp script and run it.
        """

        run_condition = all([
            self.idyom_config.run_model_configuration.required_parameters.is_complete(),
        ])
        assert run_condition
        print('** running lisp script **')
        os.system("sbcl --noinform --load " + self.generate_lisp_script())
        print(' ')
        print('** Finished! **')


def new_test():
    test_dataset_path = 'dataset/shanx_dataset/'
    target_viewpoints = ['cpitch', 'onset']
    source_viewpoints = ['cpitch', 'onset']

    my_exp = IDyOMExperiment(test_dataset_path=test_dataset_path)
    my_exp.idyom_config.run_model_configuration.required_parameters.target_viewpoints = target_viewpoints
    my_exp.idyom_config.run_model_configuration.required_parameters.source_viewpoints = source_viewpoints

    my_exp.update_idyom_config()

    print(my_exp.generate_lisp_script())

if __name__ == '__main__':
    new_test()
