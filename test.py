from py2lispIDyOM.viz import BasicPlot


def fun():
    exp = 'experiment_history/21-05-22_17.05.05/'
    # BasicPlot.selected_surprisal_entropy(experiment_folder_path=exp,
    #                                      ic_source='information.content',
    #                                      entropy_source='entropy',
    #                                      melody_names=['"chor-002"'],
    #                                      savefig=False,
    #                                      showfig=True,
    #                                      grid=True)
    #
    BasicPlot.all_entropy_plots(experiment_folder_path=exp,
                                melody_names=['"chor-002"'],
                                showfig=True,
                                savefig=False,
                                dpi=200,
                                grid=False)


if __name__ == '__main__':
    fun()
