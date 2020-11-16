(start-idyom)

(idyom-db:initialise-database)
(idyom-db:import-data :mid "TRAINFOLDER" "Train" TRAINID)
(idyom-db:import-data :mid "TESTFOLDER" "Test" TESTID)
(idyom:idyom TESTID '(cpitch onset) '(cpitch onset) :models :ltm :pretraining-ids '(TRAINID) :k 1 :detail 3 :output-path DATAOUTPUT :overwrite t)

(quit)



;(start-idyom)

;(idyom-db:delete-dataset 10)
;(idyom-db:import-data :mid "FOLDER" "Temporary dataset for evluation" 10)

;(idyom:idyom 10 '(cpitch onset) '(cpitch onset) :models :both :detail 3 :output-path "./lisp/" :overwrite t)
;(quit)



; (idyom:idyom FOLDER3 '(cpitch onset) '(cpitch onset) :models :both :detail 3 :output-path "./stimuli/giovanni/surprises/" :overwrite t)

; (idyom:idyom FOLDER3 '(cpitch onset) '(cpitch onset) :models :both :detail 3 :output-path "./lisp/" :overwrite t)

; (idyom:idyom FOLDER3 '(cpitch onset) '(cpitch onset) :k FOLDER :pretraining-ids '(FOLDER) :models :both :detail 3 :output-path "./stimuli/giovanni/surprises/" :overwrite t)

; (idyom:idyom FOLDER2 '(cpitch onset) '(cpitch onset) :pretraining-ids '(FOLDER2) :models :both :detail 3 :output-path "./lisp/" :overwrite t)

; (idyom:idyom FOLDER3 '(cpitch onset) '(cpitch onset) :k FOLDER :pretraining-ids '(FOLDER2) :models :both :detail 3 :output-path "./stimuli/giovanni/surprises/" :overwrite t)

; (idyom-db:import-data :krn "FOLDER" "Temporary dataset for evluation" FOLDER2) 
