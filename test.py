from py2lispIDyOM.run import IDyOMExperiment


def fun():
    test_dataset_path = 'examples/1_sample_experiment/dataset/bach_dataset/'
    my_exp = IDyOMExperiment(test_dataset_path=test_dataset_path)

    my_exp.set_parameters(target_viewpoints=['cpitch'],
                          source_viewpoints=['cpitch'],
                          k=':full',
                          models=':ltm',
                          model_to_configure=':ltmo',
                          order_bound=2,
                          )
    run_model_configuration = my_exp.idyom_config.run_model_configuration
    print(run_model_configuration.statistical_modelling_parameters)
    command = run_model_configuration.to_lisp_command()
    print(command)

    # my_exp.generate_lisp_script()


if __name__ == '__main__':
    fun()
