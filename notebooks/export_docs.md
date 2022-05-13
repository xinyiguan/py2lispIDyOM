# Export documentation

`class Export`

Keyword arguments:

- `experiment_folder_path`:
    - type: str
    - This is the experiment log folder path which contains the data you want to export (the folder name by default is
      the timestamp of the experiment time)
- `properties_to_export`:
    - type: list of str, e.g., `properties_to_export = ['melody.name', 'cpitch']`
    - for available properties to export, see
- `melody_names`:
    - type: list of str
    - by default, if not specified, the selected properties of all melodies data will be exported.

Given that IDyOM outputs are available (check if `.dat` file exists under the path `experiment_output_data_folder/`
in the current experiment log folder), users can extract and export certain properties in
`.mat` and/or `.csv` formats with the methods `export2mat()` and `export2csv()` respectively.

A quick example of export the "melody_name", "onset" and "cpitch" data of the two melodies
'"shanx002"', '"shanx008"' in the experiment `04-05-22_14.35.26` in `.mat` format will look like:

```
from export import Export

# define the parameters for the export
export_mat = Export(experiment_folder_path='experiment_history/04-05-22_14.35.26/',
                   properties_to_export=['onset', 'cpitch', 'melody_name'],
                   melody_names=['"shanx002"', '"shanx008"'])
                   
export_mat.export2mat()
```