(start-idyom)

(idyom-db:initialise-database)
(idyom-db:import-data :mid "experiment_history/11-17-20_13.15.34/experiment_input_data_folder/train/" "Train" 66111720131534)
(idyom-db:import-data :mid "experiment_history/11-17-20_13.15.34/experiment_input_data_folder/test/" "Test" 99111720131534)
(idyom:idyom 99111720131534 '(cpitch onset) '(cpitch onset) :models :ltm :pretraining-ids '(66111720131534) :k 1 :detail 3 :output-path "experiment_history/11-17-20_13.15.34/experiment_output_data_folder/" :overwrite t)

(quit)
