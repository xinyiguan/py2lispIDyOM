import os
from dataclasses import field, dataclass

from py2lispIDyOM.configuration import get_timestamp, IDyOMConfiguration, ExperimentLogger


@dataclass
class IDyOMExperiment:
    """
    A class to configure the IDyOM experiment.

    :param test_dataset_path: The path to your test dataset (required)
    :param pretrain_dataset_path: The path to your pretrain dataset
    :param experiment_history_folder_path: The path to which you want to save all the result data/plots, defaults to None.

    """

    test_dataset_path: str
    pretrain_dataset_path: str = None
    experiment_history_folder_path: str = None
    idyom_config: IDyOMConfiguration = field(default_factory=IDyOMConfiguration)

    def __post_init__(self):
        self.logger = ExperimentLogger(pretrain_dataset_path=self.pretrain_dataset_path,
                                       test_dataset_path=self.test_dataset_path,
                                       experiment_history_folder_path=self.experiment_history_folder_path)

    def _update_idyom_config(self):
        test_dataset_id = self._generate_test_dataset_id()
        train_dataset_id = self._generate_train_dataset_id()
        self.idyom_config.run_model_configuration.required_parameters.dataset_id = test_dataset_id
        self.idyom_config.run_model_configuration.training_parameters.pretraining_id = train_dataset_id

        self.idyom_config.database_configuration.this_exp_log_path = self.logger.this_exp_folder
        self.idyom_config.database_configuration.test_dataset_id = test_dataset_id
        self.idyom_config.database_configuration.pretrain_dataset_id = train_dataset_id
        self.idyom_config.run_model_configuration.output_parameters.output_path = self.logger.output_data_exp_folder

    @staticmethod
    def _generate_test_dataset_id() -> str:
        moment = get_timestamp()
        dataset_id = '66' + moment
        return dataset_id

    def _generate_train_dataset_id(self):
        # only generate an ID if pretrain_dataset_path is not None
        if self.pretrain_dataset_path:
            moment = get_timestamp()
            dataset_id = '99' + moment
            return dataset_id
        else:
            pass

    def set_parameters(self, **kwargs):
        """
        Set the IDyOM model parameters.
        :param kwargs: see the README or run_idyom_tutorial for a complete list of parameters (keyword arguments).

        """
        configuration = self.idyom_config.run_model_configuration
        surface_dict: dict = configuration.get_surface_dict()
        # print(f'{surface_dict=}')
        kw2hide_in_errormsg = ['output_path', 'dataset_id', 'pretraining_id', 'stmo_options', 'ltmo_options']
        kw2show = list(surface_dict.keys())
        kw2show = [ele for ele in kw2show if ele not in kw2hide_in_errormsg]
        for key, value in kwargs.items():
            if key not in surface_dict:
                raise KeyError(f'parameter \'{key}\' is invalid. Valid parameters are: {kw2show}')
            configuration.recursive_set_attr(key=key, value=value)

    def _generate_lisp_commands(self):
        """
        Generate the LISP commands for the IDyOM model configurations.
        :return: the total lisp commands for the idyom experiment
        """
        self._update_idyom_config()
        lisp_command = self.idyom_config.to_lisp_command()
        return lisp_command

    def generate_lisp_script(self, write=True):
        """
        Generate the LISP script for the IDyOM model configurations.
        :param write: whether to write the file or not, defaults to True.
        :type write: bool
        :return: the path to the lisp script file.
        """
        self._update_idyom_config()
        path_to_file = self.logger.this_exp_folder
        lisp_file_path = path_to_file + 'compute.lisp'
        lisp_command = self.idyom_config.to_lisp_command()
        if write:
            with open(lisp_file_path, "w") as f:
                f.write(lisp_command)
        return str(lisp_file_path)

    def run(self):
        """
        Run the IDyOM model.
        """

        run_condition = all([
            self.idyom_config.run_model_configuration.required_parameters.is_complete()
        ])
        assert run_condition
        print('** running lisp script **')
        os.system("sbcl --noinform --load " + self.generate_lisp_script())
        print(' ')
        print('** Finished! **')
