# Visualization Tutorial

This tutorial will cover some useful plotting in py2lispIDyOM. For an overview of the py2lispIDyOM functionality, see
the [README](README.md). In the current version, only limited basic plots are available.

### Content <br>

- [BasicPlot](#basicplot)
  1. [simple_plot](#1-simple_plot)
  2. [pianoroll_pitch_prediction_groundtruth](#2-pianoroll_pitch_prediction_groundtruth)
  3. [pianoroll_groundtruth_overall_surprisal](#3-pianoroll_groundtruth_overall_surprisal)

---

## BasicPlot

The plotting methods in `BasicPlot` all have the following common parameters. Special parameters are remarked separately
in the relevant plotting method section.

**Parameters:**

- `experiment_folder_path`: _str_ (required)
  - This is the experiment log folder path which contains the data you want to export (the folder name by default is the
    timestamp of the experiment time)
- `melody_names`: _list of str_
  - The list of melodies to plot. If not specified, plots for all melodies will be generated.
- `starting_index`: _int_
  - The starting index of the melodies in the list that you want to plot (i.e., plot the melodies starting from this
    index).
- `ending_index`: _int_
  - The ending index of the melodies in the list that you want to plot (i.e., plot the melodies until this index).
- `savefig`: _bool_
  - True if you want to save the image (default). If you don't want to save, set to False.
- `showfig`: _book_
  - True if you want to show the image. If you don't want to show, set to False (default).
- `fig_format`: _str_
  - The file format, e.g. 'png', 'pdf', 'svg', ... If unspecified, the default is 'png'
- `dpi`: _int_
  The resolution in dots per inch. Default = 400.
- `figsize`: _(float, float)_
  - The width, height in inches of the figure. You can change this accordingly.

### 1. simple_plot

This function generates a simple plot with x-axis as the onset value (indicating onset of notes in beat), and y-axis as
the selected property.

``` python3
BasicPlot.simple_plot(selected_idyom_output: str,
                      experiment_folder_path: str,
                      melody_names: List[str] = None,
                      starting_index: int = None,
                      ending_index: int = None,
                      savefig: bool = True,
                      showfig: bool = False,
                      fig_format: str = 'png',
                      dpi: float = 400,
                      figsize: tuple = (10, 5))
```

**Special Parameter:**

- `selected_idyom_output`: _str_ (required)
  - The idyom output values that you want to plot.

_Example:_

Let's plot information content (surprisal) values of the melody named '"chor-003"' in the
experiment `16-05-22_14.01.03/` .

```python3
# Import relevant py2lispIDyOM
from py2lispIDyOM.viz import BasicPlot

# Set parameters
BasicPlot.simple_plot(selected_idyom_output='information.content',
                      experiment_folder_path='examples/1_sample_experiment/16-05-22_14.01.03/',
                      melody_names=['"chor-003"'],
                      savefig=True,
                      showfig=True)
```

![simple_plot_chor_003](tutorial_plots_demo/chor-003.png)

### 2. pianoroll_pitch_prediction_groundtruth

This function returns and saves a pair of figures (the predicted pitch distribution and the ground truth).

``` python3
BasicPlot.pianoroll_pitch_prediction_groundtruth(experiment_folder_path: str,
                                                 melody_names: List[str] = None,
                                                 starting_index: int = None,
                                                 ending_index: int = None,
                                                 savefig: bool = True,
                                                 showfig: bool = False,
                                                 fig_format: str = 'png',
                                                 dpi: float = 400,
                                                 nrows: int = 2,
                                                 ncols: int = 1,
                                                 figsize: tuple = (10, 10))
```

**Parameters:**

- `nrows`: _int_
  - Number of rows of the subplot grid.
- `ncols`: _int_
  - Number of columns of the subplot grid.

If you want to have the two subplots side-by-side, set `nrows=1` and `ncols=2`. If you want to have them one on top of
another, set `nrows=2` and `ncols=1`.

_Example:_

Let's plot the 8th melody in the experiment logger `16-05-22_14.01.03/`.

In this example, we want to show the subplots side-by-side, and will need to ajust the figure size accordingly.

```python3
# Import relevant py2lispIDyOM
from py2lispIDyOM.viz import BasicPlot

# Set parameters
BasicPlot.pianoroll_pitch_prediction_groundtruth(
  experiment_folder_path='examples/1_sample_experiment/16-05-22_14.01.03/',
  starting_index=7,  # -> starting to plot the melody in 8th position.
  ending_index=8,  # -> stop plotting at the 9th (i.e., only plot the 8th)
  savefig=True,
  showfig=True,
  nrows=1,  # -> the figure will have one row of subplots
  ncols=2,  # -> the figure will have two column of subplots
  figsize=(20, 5)  # each subplot is a bit flat, so we adjust the figsize to get better fig quality
)

```

![pitch_pre_groundtruth_chor_008](tutorial_plots_demo/chor-008.png)

### 3. pianoroll_groundtruth_overall_surprisal

This function plots two subplots: ground truth pianoroll the combined(overall) information content (or surprisal) one on
top of another.

``` python3
BasicPlot.pianoroll_groundtruth_overall_surprisal(experiment_folder_path: str,
                                                  melody_names: List[str] = None,
                                                  starting_index: int = None,
                                                  ending_index: int = None,
                                                  savefig: bool = True,
                                                  showfig: bool = False,
                                                  fig_format: str = 'png',
                                                  dpi: float = 400,
                                                  figsize: tuple = (10, 5)):
```

_Example:_

Let's plot the melody named '"chor-010"' in the experiment logger `16-05-22_14.01.03/`.

```python3
# Import relevant py2lispIDyOM
from py2lispIDyOM.viz import BasicPlot

# Set parameters
BasicPlot.pianoroll_groundtruth_overall_surprisal(
  experiment_folder_path='examples/1_sample_experiment/16-05-22_14.01.03/',
  melody_names=['"chor-010"'],
  savefig=True,
  showfig=True)

```

![pianoroll_surprisal_chor_010](tutorial_plots_demo/chor-010.png)










