;;; Load CLSQL by default
(ql:quickload "clsql")

;;; IDyOM
(defun start-idyom ()
   (defvar *idyom-root* "idyom/")
   (ql:quickload "idyom")
   (clsql:connect '("idyom/db/database.sqlite") :if-exists :old :database-type :sqlite3))