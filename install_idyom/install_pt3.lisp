;;; Load CLSQL by default
(ql:quickload "clsql")
;;; IDyOM
(defun start-idyom ()
   (defvar *idyom-root* "/Users/xinyiguan/idyom/")
   (ql:quickload "idyom")
   (clsql:connect '("/Users/xinyiguan/idyom/db/database.sqlite") :if-exists :old :database-type :sqlite3))
