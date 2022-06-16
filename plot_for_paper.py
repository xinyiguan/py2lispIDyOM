from py2lispIDyOM.viz import BasicPlot


def plots():
    experiment_folder_path = '21-05-22_17.05.05/'

    pitch_pred_plot = BasicPlot.pianoroll_pitch_prediction_groundtruth(experiment_folder_path=experiment_folder_path,
                                                                       melody_names=['"chor-003"'],
                                                                       savefig=True,
                                                                       fig_format='svg',
                                                                       dpi=400,
                                                                       probability_colorbar=True
                                                                       )


if __name__=='__main__':
    plots()