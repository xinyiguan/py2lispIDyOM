(start-idyom)

(idyom-db:initialise-database)
(idyom-db:import-data :mid "experiment_history/03-07-21_15.42.10/experiment_input_data_folder/train/" "Train" 66030721154210)
(idyom-db:import-data :mid "experiment_history/03-07-21_15.42.10/experiment_input_data_folder/test/" "Test" 99030721154210)
(idyom:idyom 99030721154210 '(cpitch) '(cpitch) :models :both :pretraining-ids '(66030721154210) :k 1 :detail 3 :output-path "experiment_history/03-07-21_15.42.10/experiment_output_data_folder/" :overwrite t)

(quit)
