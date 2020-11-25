(start-idyom)

(idyom-db:initialise-database)
(idyom-db:import-data :mid "experiment_history/11-18-20_14.50.38/experiment_input_data_folder/train/" "Train" 66111820145038)
(idyom-db:import-data :mid "experiment_history/11-18-20_14.50.38/experiment_input_data_folder/test/" "Test" 99111820145038)
(idyom:idyom 99111820145038 '(cpitch onset) '(cpitch onset) :models :ltm :pretraining-ids '(66111820145038) :k 1 :detail 3 :output-path "experiment_history/11-18-20_14.50.38/experiment_output_data_folder/" :overwrite t)

(quit)
