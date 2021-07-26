(start-idyom)

(idyom-db:import-data :mid "experiment_history/07-26-21_17.29.13/experiment_input_data_folder/train/" "Train" 66072621172913)
(idyom-db:import-data :mid "experiment_history/07-26-21_17.29.13/experiment_input_data_folder/test/" "Test" 99072621172913)
(idyom:idyom 99072621172913 '(cpitch onset dur) '(cpitch onset dur) :models :both :pretraining-ids '(66072621172913) :k 1 :detail 3 :output-path "experiment_history/07-26-21_17.29.13/experiment_output_data_folder/" :overwrite t)

(quit)