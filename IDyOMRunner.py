from dataclasses import dataclass, field

from configuration import *
import os

@dataclass
class IDyOMRunner:
    database_configuration: DatabaseConfiguration = field(default_factory=DatabaseConfiguration)
    run_model_configuration: RunModelConfiguration = field(default_factory=RunModelConfiguration)

    def run(self):
        self.open_sbcl_command()
        self.start_idyom_command()
        self.initialize_database_command()
        self.run_model_command()

    def total_command(self)->str:
        commands = [
            self.open_sbcl_command(),
            self.start_idyom_command(),
            self.initialize_train_database_command(),
            self.initialize_test_database_command(),
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

    def initialize_train_database_command(self)->str:
        command = self.database_configuration.to_lisp_command()[1]
        return command

    def initialize_test_database_command(self)->str:
        command = self.database_configuration.to_lisp_command()[0]
        return command

    def run_model_command(self)->str:
        command = self.run_model_configuration.to_lisp_command()
        return command



def test():
    required_parameters = RequiredParameters(dataset_path='dataset/bach_dataset',
                                             target_viewpoints=['cpitch', 'onset'],
                                             source_viewpoints=['cpitch', 'onset', ('cpitch', 'articulation')])

    statistical_parameters = StatisticalModellingParameters(models=':both')

    run_model_configuration = RunModelConfiguration(required_parameters=required_parameters)
    database_configuration = DatabaseConfiguration(run_model_configuration)
    idyom_runner = IDyOMRunner(database_configuration=database_configuration, run_model_configuration=run_model_configuration)
    idyom_runner.total_command()


if __name__ == '__main__':
    test()
