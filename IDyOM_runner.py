from dataclasses import dataclass, field
from typing import Callable

from configuration import RunModelConfiguration, DatabaseConfiguration
import os

@dataclass
class IdyomRunner:
    database_configuration: DatabaseConfiguration = field(default_factory=DatabaseConfiguration)
    run_model_configuration: RunModelConfiguration = field(default_factory=RunModelConfiguration)

    def run(self):
        self.open_sbcl()
        self.start_idyom()
        self.initialize_database()
        self.run_model()

    def total_command(self)->str:
        commands = [
            self.open_sbcl_command(),
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

def test():
    idyom_runner = IdyomRunner()
    idyom_runner.total_command()


if __name__ == '__main__':
    test()
