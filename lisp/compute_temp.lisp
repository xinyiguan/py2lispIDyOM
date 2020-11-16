(start-idyom)

(idyom-db:initialise-database)
(idyom-db:import-data :mid "experiment_history/11-16-20_16.36.04/experiment_input_data_folder/train/" "Train" 66111620163604)
(idyom-db:import-data :mid "experiment_history/11-16-20_16.36.04/experiment_input_data_folder/test/" "Test" 99111620163604)
(idyom:idyom 99111620163604 '(cpitch onset) '(cpitch onset) :models :ltm :pretraining-ids '(66111620163604) :k 1 :detail 3 :output-path "experiment_history/11-16-20_16.36.04/experiment_output_data_folder/" :overwrite t)

(quit)
