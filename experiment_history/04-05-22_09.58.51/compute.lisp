(start-idyom)
(idyom-db:import-data :mid "experiment_history/04-05-22_09.58.51/experiment_input_data_folder/test/" "TEST_DATASET" 66050422095851)
(idyom-db:import-data :mid "experiment_history/04-05-22_09.58.51/experiment_input_data_folder/train/" "PRETRAIN_DATASET" 99050422095851)
(idyom:idyom 66050422095851 '(cpitch onset) '(cpitch onset) :models :both :pretraining-ids '(99050422095851) :k 1 :detail 3 :output-path "experiment_history/04-05-22_09.58.51/experiment_output_data_folder/" :overwrite nil)
(quit)