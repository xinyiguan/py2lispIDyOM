(start-idyom)

(idyom-db:initialise-database)
(idyom-db:import-data :mid "experiment_history/03-08-21_13.40.14/experiment_input_data_folder/train/" "Train" 66030821134014)
(idyom-db:import-data :mid "experiment_history/03-08-21_13.40.14/experiment_input_data_folder/test/" "Test" 99030821134014)
(idyom:idyom 99030821134014 '(cpitch onset) '(cpitch onset) :models :both :pretraining-ids '(66030821134014) :k 1 :detail 3 :output-path "experiment_history/03-08-21_13.40.14/experiment_output_data_folder/" :overwrite t)

(quit)
