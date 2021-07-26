(start-idyom)

(idyom-db:import-data :mid "experiment_history/07-26-21_17.32.52/experiment_input_data_folder/train/" "Train" 66072621173252)
(idyom-db:import-data :mid "experiment_history/07-26-21_17.32.52/experiment_input_data_folder/test/" "Test" 99072621173252)
(idyom:idyom 99072621173252 '(cpitch onset dur) '(cpitch onset dur) :models :both :pretraining-ids '(66072621173252) :k 1 :detail 3 :output-path "experiment_history/07-26-21_17.32.52/experiment_output_data_folder/" :overwrite t)

(quit)