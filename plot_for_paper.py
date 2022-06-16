from py2lispIDyOM.viz import BasicPlot


def plots():
    experiment_folder_path = '21-05-22_17.05.05/'

    # pitch_pred_plot = BasicPlot.pianoroll_pitch_prediction_groundtruth(experiment_folder_path=experiment_folder_path,
    #                                                                    melody_names=['"chor-003"'],
    #                                                                    savefig=True,
    #                                                                    fig_format='png',
    #                                                                    dpi=400,
    #                                                                    probability_colorbar=True
    #                                                                    )
    # all_surprisals = BasicPlot.all_surprisal(experiment_folder_path=experiment_folder_path,
    #                                          melody_names=['"chor-003"'],
    #                                          savefig=True,
    #                                          fig_format='png',
    #                                          dpi=400,
    #                                          figsize=(10,7))
    #
    #
    suprisal_entropy = BasicPlot.selected_surprisal_entropy(experiment_folder_path=experiment_folder_path,
                                                            ic_source='information.content',
                                                            entropy_source='entropy',
                                                            melody_names=['"chor-003"'],
                                                            savefig=True,
                                                            fig_format='png',
                                                            dpi=400,
                                                            figsize=(10, 6))


    # groundtruth_surprisal = BasicPlot.pianoroll_groundtruth_overall_surprisal(
    #     experiment_folder_path=experiment_folder_path,
    #     melody_names=['"chor-003"'],
    #     savefig=True,
    #     fig_format='png',
    #     dpi=400,
    #     figsize=(10, 8))
if __name__ == '__main__':
    plots()
