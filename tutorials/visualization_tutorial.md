# Visualization Tutorial

This tutorial will cover some useful plotting in py2lispIDyOM. For an overview of the py2lispIDyOM functionality, see
the [README](README.md).

### Content <br>

---

### 1. simple_plot

This function generates a simple plot with x-axis as the onset value (indicating time), and y-axis as the selected
property.

```python3
BasicPlot.simple_plot(selected_property,
                      experiment_folder_path,
                      melody_names=None,
                      starting_index=None,
                      ending_index=None,
                      savefig=True,
                      showfig=False)
```

**Parameters:**

- `selected_property`: _str_
    - The property values that you want to plot.
- `experiment_folder_path`: _str_
    - This is the experiment log folder path which contains the data you want to export (the folder name by default is
      the timestamp of the experiment time)
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

_Example:_

```python3
from modules.viz import BasicPlot

BasicPlot.simple_plot(selected_property='information.content',
                      experiment_folder_path='examples/1_sample_experiment/16-05-22_14.01.03/',
                      melody_names=['"chor-003"'],
                      savefig=True,
                      showfig=True)

```