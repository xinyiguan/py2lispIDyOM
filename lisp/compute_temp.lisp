(start-idyom)

(idyom-db:initialise-database)
(idyom-db:import-data :mid "experiment_history/11-16-20_15.00.56/experiment_input_data_folder/train/" "Train" 66111620150056)
(idyom-db:import-data :mid "experiment_history/11-16-20_15.00.56/experiment_input_data_folder/test/" "Test" 99111620150056)
(idyom:idyom 99111620150056 '(cpitch onset) '(cpitch onset) :models :ltm :pretraining-ids '(66111620150056) :k 1 :detail 3 :output-path "experiment_history/11-16-20_15.00.56/experiment_output_data_folder/" :overwrite t)

(quit)
