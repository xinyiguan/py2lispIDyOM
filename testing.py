from modules.viz import BasicPlot


def fun():
    # BasicPlot.pianoroll_pitch_prediction_groundtruth(experiment_folder_path='examples/1_sample_experiment/16-05-22_14.01.03/',
    #                                                  melody_names=['"chor-008"'],
    #                                                  savefig=True,
    #                                                  showfig=False,
    #                                                  fig_format='png',
    #                                                  dpi=400,
    #                                                  )

    # BasicPlot.pianoroll_pitch_prediction_groundtruth(experiment_folder_path='experiment_history/04-05-22_14.35.26/',
    #                                                  melody_names=['"shanx002"'],
    #                                                  savefig=True,
    #                                                  showfig=False,
    #                                                  fig_format='png',
    #                                                  dpi=400,
    #                                                  nrows=1,
    #                                                  ncols=2,
    #                                                  figsize=(10,5))

    BasicPlot.simple_plot(selected_idyom_output='onset.entropy',
                          experiment_folder_path='examples/1_sample_experiment/16-05-22_14.01.03/',
                          melody_names=['"chor-002"'],
                          savefig=True)

    # BasicPlot.pianoroll_groundtruth_overall_surprisal(experiment_folder_path='examples/1_sample_experiment/16-05-22_14.01.03/',
    #                                                   melody_names=['"chor-002"'],
    #                                                   )


if __name__ == '__main__':
    fun()
