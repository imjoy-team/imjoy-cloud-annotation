# %% Python code processing and organizing segmentation results for 
# the ImJoy clodu annotation tool. 
# 
# === Objectives
#  This code has two objectives
#   1. Transform label images in geojson files.
#   2. Reorganize that such that it can be used in the cloud annotation tool.
#
#  Code is adapted to work with provided example data, and thus meant as a starting
#  point for your own development. Modications to adapt the code to your own
#  file organization and naming convention is likely necessary.
#
# === Example data
#  Available here: https://www.dropbox.com/sh/hkr7xmpp9y5movz/AAAzHhbd-BhxNoA-1ZBQgviya?dl=0
#   Folder "segmentation-results" is the input, "segmentation-annotation" the created folder
#   with the reorganized data.
# 
#   Provided are segmentation results in one folder, 
#    1. Image that was segmented having a unique name, e.g. sample_1_dapi.tif 
#    2. Segmented image has a suffix (__nuc_label), e.g. sample_1_dapi__nuc_label.png



# %% Imports
from skimage.io import imread, imsave
from skimage.exposure import rescale_intensity
from shutil import copyfile
from pathlib import Path
from geojson import dump

from utils_annotation import label_to_geojson


# %% Process segmentation results

# >>>> Specify data
path_results = Path(r'PASTE-PATH-TO-DATA')        # Folder with segmentation results
path_save = Path(r'PASTE-PATH-TO-SAVE-RESULTS')   # Folder to store data

# %%
img_ext = '.tif'                  # File extension of segmented image, if not png, image will be saved as 8bit png image
label_ext = '.png'                # File extension of segmentation resuls (label image)

string_img = '_dapi'              # unique identifier of segmented image  
string_label = '_dapi__nuc_label'  # unique identifier of label image.

# >>> Check folders
if not path_results.is_dir():
    print(f'Path to images does not exist: {path_results}')

# >>> Folder to store results for annotation

if not path_save.is_dir():
    path_save.mkdir(parents=True)
else:
    print(f'WARNING. Path to save data for annotation already exists {path_save}. Content will be added. ')
    
# >>> Loop over all images
for file_img in path_results.glob(f'*{string_img}*{img_ext}'):
    print(f'\n=== Analyzing image: {file_img}')
    
    # >>> Generate name of segmentation mask
    name_label = Path(str(file_img.name).replace(string_img, string_label).replace(img_ext, label_ext))
    
    if str(name_label) == str(file_img.name):
        print('Name of segmentation is identical to input image. This is a likely a mistake.')
        continue
    
    file_label = path_results / name_label
    if not file_label.is_file():
        print(f'File with segmentation results does not exist: {file_label}')
        continue
    
    img_label = imread(str(file_label))
    
    # >>> Transform into geojson
    feature_collection, features = label_to_geojson(img_label, label='nuclei', simplify_tol=1.5)
    
    # >>> Open original file
    
    # >>> Save files in new folder 
    path_save_loop = path_save / file_img.stem.replace(string_img, '')
    print(f'Annotations will be saved in folder : {path_save_loop}')
    if not path_save_loop.is_dir():
        path_save_loop.mkdir(parents=True)
    
    # Save feature_collection as json file
    file_annotation = path_save_loop / "annotation.json"
    with open(file_annotation, 'w') as f:
        dump(feature_collection, f)
        f.close()

    # Copy original image file
    # copyfile(file_img, path_save_loop / f'dapi{img_ext}')
    
    # Save image file as png
    if img_ext != ('.png'):
        img_input = imread(str(file_img))
        
        # Save rescaled 8 bit image as png
        imsave(str(path_save_loop / 'dapi.png'), 
               rescale_intensity(img_input, in_range='image', out_range='uint8'))
    else:
        copyfile(file_img, path_save_loop / f'dapi.{img_ext}')

