# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
# %% Get label images array from the uploaded dataset folder
#
#
# === Objectives
#  This code has two objectives
#   1. Transform geojson files in numpy array.
#   2. Save arrays in the same folder than the geojson files they come from.
#


# %% Imports

import numpy as np
from pathlib import Path
from utils_annotation import geojson_to_label
import json

# %%
path_results = Path(r'PASTE-PATH-TO-DATA')  # Folder with segmentation results from imjoy-cloud-annotation

if not path_results.is_dir():
    print(f'Path to label does not exist: {path_results}')

for folder in path_results.glob("*/"):
    print(f'\n=== Analyzing image: {folder}')
    #  get image size
    annotaion_folder = folder / "target_files_v0"
    for json_file in annotaion_folder.glob('*.json'):
        with open(str(json_file), encoding='utf-8-sig') as fh:
            data_json = json.load(fh)
            if 'bbox' in data_json:
                img_size = (int(data_json['bbox'][2]-data_json['bbox'][0]+1),
                            int(data_json['bbox'][3]-data_json['bbox'][1]+1))
                img_size = (img_size[1], img_size[0])
    # save array of label
    for annotaion_folder in folder.glob("*target_files_v*"):
        for json_file in annotaion_folder.glob('*.json'):
            with open(str(json_file), encoding='utf-8-sig') as fh:
                data_json = json.load(fh)
                label = geojson_to_label(data_json, img_size, binary_labeling=False)
                np.save(str(json_file)[:-5], label.astype(int))