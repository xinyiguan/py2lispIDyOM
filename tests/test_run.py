import datetime
import shutil
import unittest
from unittest import TestCase
from py2lispIDyOM.run import IDyOMExperiment


class TestIDyOMExperiment(TestCase):

    def test_case_1(self):
        """Test case 1:
        experiment logger name is 'TestCase1'
        target_viewpoints='(cpitch), source_viewpoints='((cpintfref cpint) cpitch)
        model=stm, stmo=stmo, order_bound=5, k = 2, detail=3
        """

        test_dataset_path = 'dataset/bach_dataset/'
        experiment_logger_path = 'experiment_history/TestCase1/'
        shutil.rmtree(experiment_logger_path, ignore_errors=True)
        idyom_experiment = IDyOMExperiment(test_dataset_path=test_dataset_path, experiment_logger_name='TestCase1')
        idyom_experiment.set_parameters(target_viewpoints=['cpitch'],
                                        source_viewpoints=[('cpintfref', 'cpint'), 'cpitch'],
                                        models=':stm',
                                        stmo=':stmo',
                                        stmo_order_bound=5,
                                        k=2,
                                        detail=3)

        exp_folder_name = 'TestCase1'

        test_dataset_id = idyom_experiment._generate_test_dataset_id()
        generated_commands = idyom_experiment._generate_lisp_commands()
        expected_commands = f'(start-idyom)\n' \
                            f'(idyom-db:import-data :mid "experiment_history/{exp_folder_name}/experiment_input_data_folder/test_dataset/" ' \
                            f'"TEST_DATASET" {test_dataset_id})\n' \
                            f'(idyom:idyom {test_dataset_id} \'(cpitch) \'((cpintfref cpint) cpitch) :models :stm :stmo ' \
                            f'\'(:order-bound 5) :k 2 :detail 3 :output-path "experiment_history/{exp_folder_name}/experiment_output_data_folder/" :overwrite nil)\n' \
                            f'(quit)'

        self.assertEqual(generated_commands, expected_commands)

    def test_case_2(self):
        """Test case 2:
        experiment logger name is by default (timestamp)
        target_viewpoints='(cpitch onset), source_viewpoints='(cpitch onset)
        model=both, ltmo=ltmo, order_bound=8, k = full, detail=3
        """

        test_dataset_path = 'dataset/bach_dataset/'
        pretrain_dataset_path = 'dataset/shanx_dataset/'

        idyom_experiment = IDyOMExperiment(test_dataset_path=test_dataset_path,
                                           pretrain_dataset_path=pretrain_dataset_path)
        idyom_experiment.set_parameters(target_viewpoints=['cpitch', 'onset'],
                                        source_viewpoints=['cpitch', 'onset'],
                                        models=':both',
                                        ltmo=':ltmo',
                                        ltmo_order_bound=8,
                                        k=':full',
                                        detail=3)

        today_date = datetime.date.today()
        now_time = datetime.datetime.now()
        exp_folder_name = today_date.strftime(
            '%d-%m-%y') + '_' + now_time.strftime(
            '%H.%M.%S')

        test_dataset_id = idyom_experiment._generate_test_dataset_id()
        pretrain_dataset_id = idyom_experiment._generate_train_dataset_id()
        generated_commands = idyom_experiment._generate_lisp_commands()
        expected_commands = f'(start-idyom)\n' \
                            f'(idyom-db:import-data :mid "experiment_history/{exp_folder_name}/experiment_input_data_folder/test_dataset/" ' \
                            f'"TEST_DATASET" {test_dataset_id})\n' \
                            f'(idyom-db:import-data :mid "experiment_history/{exp_folder_name}/experiment_input_data_folder/pretrain_dataset/" ' \
                            f'"PRETRAIN_DATASET" {pretrain_dataset_id})\n' \
                            f'(idyom:idyom {test_dataset_id} \'(cpitch onset) \'(cpitch onset) :models :both :ltmo ' \
                            f'\'(:order-bound 8) :pretraining-ids \'({pretrain_dataset_id}) :k :full :detail 3 :output-path "experiment_history/{exp_folder_name}/experiment_output_data_folder/" :overwrite nil)\n' \
                            f'(quit)'

        self.assertEqual(generated_commands, expected_commands)


if __name__ == '__main__':
    unittest.main()
