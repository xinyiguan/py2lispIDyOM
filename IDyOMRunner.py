from dataclasses import dataclass, field

from configuration import *
import os

@dataclass
class IDyOMRunner:
    run_model_configuration: RunModelConfiguration = field(default_factory=RunModelConfiguration)
    database_configuration: DatabaseConfiguration = field(default_factory=DatabaseConfiguration)


    def total_command(self)->str:
        commands = [
            # self.open_sbcl_command(),
            self.start_idyom_command(),
            self.initialize_database_command(),
            self.run_model_command(),
        ]
        total_command = '\n'.join(commands)
        return total_command


    def open_sbcl_command(self)->str:
        command = 'sbcl'
        return command

    def start_idyom_command(self)->str:
        command = '(start-idyom)'
        return command

    def initialize_database_command(self)->str:
        command = self.database_configuration.to_lisp_command()
        return command

    def run_model_command(self)->str:
        command = self.run_model_configuration.to_lisp_command()
        return command

    def generate_lisp_script(self):
        path_to_file = 'experiment_history/'
        lisp_file_path = path_to_file+'compute.lisp'
        with open(lisp_file_path, "w") as f:  # Opens file and casts as f
            f.write(self.total_command())
        return lisp_file_path

    def run(self):
        """use shell to run IDyOM LISP code """
        print('** running lisp script **')
        os.system("sbcl --noinform --load " + self.generate_lisp_script())
        print(' ')
        print('** Finished! **')


def test():
    required_parameters = RequiredParameters(dataset_path='dataset/bach_dataset/',
                                             target_viewpoints=['cpitch', 'onset'],
                                             source_viewpoints=['cpitch', 'onset', ('cpitch', 'articulation')])
    training_parameters = TrainingParameters(pretraining_dataset_path='dataset/shanx_dataset/',
                                             k=2)
    statistical_parameters = StatisticalModellingParameters(models=':both')
    run_model_config = RunModelConfiguration(required_parameters=required_parameters,
                                             training_parameters=training_parameters)
    db_config = DatabaseConfiguration(run_model_configuration=run_model_config)
    idyom_runner = IDyOMRunner(run_model_configuration=run_model_config,database_configuration=db_config)


if __name__ == '__main__':
    test()
