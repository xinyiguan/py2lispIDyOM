# def generate_IDyOM_LISP_script(outpath):
#     IDyOM_Lisp_script = open('./experiment_history.IDyOM_Lisp_script.lisp', 'w')
#     lisp_start_idyom = '(start-idyom)'
#     lisp_import_test_dataset =
#
#     IDyOM_Lisp_script.write(lisp_script)


# def runLisp(lisp_file_path):
#     """use shell to run IDyOM LISP code """
#     print('** running lisp **')
#     os.system("sbcl --noinform --load " + lisp_file_path)
#     print(' ')
#     print('** we got here! done! **')

if __name__ == '__main__':
    initialize_experiment_folder(experiment_history_folder='new_exp_folder')
