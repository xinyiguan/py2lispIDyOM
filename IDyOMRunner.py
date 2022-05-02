from dataclasses import field, dataclass

import configuration as configuration
import os


@dataclass
class IDyOMRunner:
    run_model_configuration: configuration.RunModelConfiguration = field(
        default_factory=configuration.RunModelConfiguration)

    def __post_init__(self):
        self.database_configuration = configuration.DatabaseConfiguration(run_model_configuration=self.run_model_configuration)

    def total_lisp_command(self) -> str:
        commands = [
            self.start_idyom_command(),
            self.initialize_database_command(),
            self.run_model_command(),
            self.quit_command()
        ]
        total_command = '\n'.join(commands)
        return total_command

    def start_idyom_command(self) -> str:
        command = '(start-idyom)'
        return command

    def initialize_database_command(self) -> str:
        command = self.database_configuration.to_lisp_command()
        return command

    def run_model_command(self) -> str:
        command = self.run_model_configuration.to_lisp_command()
        return command

    def quit_command(self) -> str:
        command = '(quit)'
        return command

    def generate_lisp_script(self):
        path_to_file = self.database_configuration.experiment_folder.this_exp_folder
        lisp_file_path = path_to_file + 'compute.lisp'
        lisp_command = self.total_lisp_command()
        with open(lisp_file_path, "w") as f:
            f.write(lisp_command)
        return str(lisp_file_path)

    def run(self):
        """use shell to run IDyOM LISP code """
        print('** running lisp script **')
        os.system("sbcl --noinform --load " + self.generate_lisp_script())
        print(' ')
        print('** Finished! **')

    def run_start_idyom_command(self):
        print('** Starting IDyOM in SBCL **')
        os.system('sbcl')
        os.system(self.start_idyom_command())


def test():
    required_parameters = configuration.RequiredParameters(dataset_path='dataset/bach_dataset/',
                                                           target_viewpoints=['cpitch', 'onset'],
                                                           source_viewpoints=['cpitch', 'onset'])

    training_parameters = configuration.TrainingParameters(pretraining_dataset_path='dataset/shanx_dataset/',
                                                           k=1)
    statistical_modelling_parameters = configuration.StatisticalModellingParameters(models=':both')

    output_parameters = configuration.OutputParameters(detail=3, output_path='experiment_history/')
    run_model_config = configuration.RunModelConfiguration(required_parameters=required_parameters,
                                                           statistical_modelling_parameters=statistical_modelling_parameters,
                                                           training_parameters=training_parameters,
                                                           output_parameters=output_parameters
                                                           )

    idyom_runner = IDyOMRunner(run_model_configuration=run_model_config)

if __name__ == '__main__':
    test()