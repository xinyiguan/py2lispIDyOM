"""
This test script concerns the configuration and run functionality.
"""
import datetime, os, shutil
from unittest import TestCase
from py2lispIDyOM.run import IDyOMExperiment


class Test(TestCase):
    bach_dataset = './tests/dataset/bach_dataset/'
    shanx_dataset = './tests/dataset/shanx_dataset/'
    Chabrier_krn = './tests/dataset/Chabrier_krn/'
    Masse_krn = './tests/dataset/Masse_krn/'
    empty_dataset = './test/dataset/empty_dataset/'

    experiment_logger_path = 'experiment_history/'

    def test_case_1(self):
        """Test case 1:
        experiment logger name is 'TestCase1'
        target_viewpoints='(cpitch), source_viewpoints='((cpintfref cpint) cpitch)
        model=stm, stmo=stmo, order_bound=5, k = 2, detail=3
        """

        test_dataset_path = self.bach_dataset
        exp_folder_name = 'TestCase1'
        experiment_logger_path = self.experiment_logger_path + exp_folder_name + '/'

        if os.path.exists(experiment_logger_path):
            shutil.rmtree(experiment_logger_path, ignore_errors=True)

        idyom_experiment = IDyOMExperiment(test_dataset_path=test_dataset_path, experiment_logger_name=exp_folder_name)
        idyom_experiment.set_parameters(target_viewpoints=['cpitch'],
                                        source_viewpoints=[('cpintfref', 'cpint'), 'cpitch'],
                                        models=':stm',
                                        stmo=':stmo',
                                        stmo_order_bound=5,
                                        k=2,
                                        detail=3)

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

        test_dataset_path = self.bach_dataset
        pretrain_dataset_path = self.shanx_dataset

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

    def test_case_3(self):
        test_dataset_path = self.Chabrier_krn
        pretrain_dataset_path = self.Masse_krn

        exp_folder_name = 'TestCase3'
        experiment_logger_path = self.experiment_logger_path + exp_folder_name + '/'

        if os.path.exists(experiment_logger_path):
            shutil.rmtree(experiment_logger_path, ignore_errors=True)

        idyom_experiment = IDyOMExperiment(test_dataset_path=test_dataset_path,
                                           pretrain_dataset_path=pretrain_dataset_path,
                                           experiment_logger_name=exp_folder_name)
        idyom_experiment.set_parameters(target_viewpoints=['cpitch', 'onset'],
                                        source_viewpoints=['cpitch', 'onset'],
                                        models=':both',
                                        ltmo=':ltmo',
                                        stmo=':stmo',
                                        ltmo_order_bound=3,
                                        stmo_order_bound=2,
                                        detail=2,
                                        overwrite=True)

        idyom_experiment.generate_lisp_script(write=True)

        test_dataset_id = idyom_experiment._generate_test_dataset_id()
        pretrain_dataset_id = idyom_experiment._generate_train_dataset_id()
        generated_commands = idyom_experiment._generate_lisp_commands()

        expected_commands = f'(start-idyom)\n' \
                            f'(idyom-db:import-data :krn "experiment_history/{exp_folder_name}/experiment_input_data_folder/test_dataset/" ' \
                            f'"TEST_DATASET" {test_dataset_id})\n' \
                            f'(idyom-db:import-data :krn "experiment_history/{exp_folder_name}/experiment_input_data_folder/pretrain_dataset/" ' \
                            f'"PRETRAIN_DATASET" {pretrain_dataset_id})\n' \
                            f'(idyom:idyom {test_dataset_id} \'(cpitch onset) \'(cpitch onset) :models :both :stmo \'(:order-bound 2) :ltmo ' \
                            f'\'(:order-bound 3) :pretraining-ids \'({pretrain_dataset_id}) :k 10 :detail 2 :output-path "experiment_history/{exp_folder_name}/experiment_output_data_folder/" :overwrite t)\n' \
                            f'(quit)'
        self.assertEqual(generated_commands, expected_commands)

    def test_case_4(self):
        test_dataset_path = self.Chabrier_krn
        pretrain_dataset_path = self.Masse_krn

        exp_folder_name = 'TestCase4'
        experiment_logger_path = self.experiment_logger_path + exp_folder_name + '/'

        if os.path.exists(experiment_logger_path):
            shutil.rmtree(experiment_logger_path, ignore_errors=True)

        idyom_experiment = IDyOMExperiment(test_dataset_path=test_dataset_path,
                                           pretrain_dataset_path=pretrain_dataset_path,
                                           experiment_logger_name=exp_folder_name)
        idyom_experiment.set_parameters(target_viewpoints=['cpitch', 'onset'],
                                        source_viewpoints=['cpitch', 'onset'],
                                        models=':both',
                                        detail=2,
                                        overwrite=True)

        idyom_experiment.generate_lisp_script(write=True)

        test_dataset_id = idyom_experiment._generate_test_dataset_id()
        pretrain_dataset_id = idyom_experiment._generate_train_dataset_id()
        generated_commands = idyom_experiment._generate_lisp_commands()

        expected_commands = f'(start-idyom)\n' \
                            f'(idyom-db:import-data :krn "experiment_history/{exp_folder_name}/experiment_input_data_folder/test_dataset/" ' \
                            f'"TEST_DATASET" {test_dataset_id})\n' \
                            f'(idyom-db:import-data :krn "experiment_history/{exp_folder_name}/experiment_input_data_folder/pretrain_dataset/" ' \
                            f'"PRETRAIN_DATASET" {pretrain_dataset_id})\n' \
                            f'(idyom:idyom {test_dataset_id} \'(cpitch onset) \'(cpitch onset) :models :both ' \
                            f':pretraining-ids \'({pretrain_dataset_id}) :k 10 :detail 2 :output-path "experiment_history/{exp_folder_name}/experiment_output_data_folder/" :overwrite t)\n' \
                            f'(quit)'
        self.assertEqual(generated_commands, expected_commands)

    def test_config_command_lines(self):
        test_dataset_path = self.Chabrier_krn
        pretrain_dataset_path = self.Masse_krn

        exp_folder_name = 'TestCaseCL'
        experiment_logger_path = self.experiment_logger_path + exp_folder_name + '/'

        if os.path.exists(experiment_logger_path):
            shutil.rmtree(experiment_logger_path, ignore_errors=True)

        idyom_experiment = IDyOMExperiment(test_dataset_path=test_dataset_path,
                                           pretrain_dataset_path=pretrain_dataset_path,
                                           experiment_logger_name=exp_folder_name)

        result1 = idyom_experiment.idyom_config.describe_database_command()
        answers1 = '(idyom-db:describe-database)'
        self.assertEqual(result1, answers1)

        result2 = idyom_experiment.idyom_config.describe_detailed_database_command()
        answers2 = '(idyom-db:describe-database :verbose t)'
        self.assertEqual(result2, answers2)


    def test_raise_error1(self):
        test_dataset_path = self.bach_dataset
        pretrain_dataset_path = self.shanx_dataset
        exp_folder_name = 'TestCaseError1'
        experiment_logger_path = self.experiment_logger_path + exp_folder_name + '/'

        if os.path.exists(experiment_logger_path):
            shutil.rmtree(experiment_logger_path, ignore_errors=True)

        idyom_experiment = IDyOMExperiment(test_dataset_path=test_dataset_path,
                                           pretrain_dataset_path=pretrain_dataset_path,
                                           experiment_logger_name=exp_folder_name)

        with self.assertRaises(KeyError):
            # supposed to raise KeyError -- 'models' (run-82)
            idyom_experiment.set_parameters(target_viewpoints=['cpitch'],
                                            source_viewpoints=['cpitch'],
                                            model=':ltmo',
                                            ltmo_order_bound=3,
                                            detail=3)

    def test_raise_error2(self):
        test_dataset_path = self.bach_dataset
        exp_folder_name = 'TestCaseError2'
        experiment_logger_path = self.experiment_logger_path + exp_folder_name + '/'

        if os.path.exists(experiment_logger_path):
            shutil.rmtree(experiment_logger_path, ignore_errors=True)

        idyom_experiment = IDyOMExperiment(test_dataset_path=test_dataset_path, experiment_logger_name=exp_folder_name)

        with self.assertRaises(TypeError):
            # supposed to raise TypeError -- 'target_viewpoints' type should be List[SingleViewpoint] (configuration-76)
            idyom_experiment.set_parameters(target_viewpoints='cpitch',
                                            source_viewpoints=['cpitch'],
                                            models=':stm',
                                            basis=[':onset'],
                                            detail=3)

        with self.assertRaises(AssertionError):
            # supposed to raise AssertionError -- 'target_viewpoints','source_viewpoints' missing (configuration-202)
            idyom_experiment.set_parameters(models=':both',
                                            detail=3)
            idyom_experiment._generate_lisp_commands()


    def test_raise_error_empty_test_dataset(self):
        test_dataset_path = self.empty_dataset
        exp_folder_name = 'TestCaseErrorTestDataset'
        experiment_logger_path = self.experiment_logger_path + exp_folder_name + '/'

        if os.path.exists(experiment_logger_path):
            shutil.rmtree(experiment_logger_path, ignore_errors=True)

        with self.assertRaises(AssertionError):
            # supposed to raise AssertionError -- empty dataset (configuration-442)
            IDyOMExperiment(test_dataset_path=test_dataset_path,
                            experiment_logger_name=exp_folder_name)

    def test_raise_error_empty_pretrain_dataset(self):
        test_dataset_path = self.bach_dataset
        pretrain_dataset_path = self.empty_dataset
        exp_folder_name = 'TestCaseErrorPretrainDataset'
        experiment_logger_path = self.experiment_logger_path + exp_folder_name + '/'

        if os.path.exists(experiment_logger_path):
            shutil.rmtree(experiment_logger_path, ignore_errors=True)

        with self.assertRaises(AssertionError):
            # supposed to raise AssertionError -- empty pretrain dataset (configuration-460)

            IDyOMExperiment(test_dataset_path=test_dataset_path,
                            pretrain_dataset_path=pretrain_dataset_path,
                            experiment_logger_name=exp_folder_name)

    def test_run(self):
        test_dataset_path = self.bach_dataset
        pretrain_dataset_path = self.shanx_dataset

        exp_folder_name = 'TestRun'
        experiment_logger_path = self.experiment_logger_path + exp_folder_name + '/'

        if os.path.exists(experiment_logger_path):
            shutil.rmtree(experiment_logger_path, ignore_errors=True)

        idyom_experiment = IDyOMExperiment(test_dataset_path=test_dataset_path,
                                           pretrain_dataset_path=pretrain_dataset_path,
                                           experiment_logger_name=exp_folder_name)

        idyom_experiment.set_parameters(target_viewpoints=['cpitch'],
                                        source_viewpoints=['cpitch'],
                                        models=':both',
                                        detail=2,
                                        overwrite=True)
        idyom_experiment.run()