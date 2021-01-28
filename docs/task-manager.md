[![powered by ImJoy](https://imjoy.io/static/badge/powered-by-imjoy-badge.svg)](https://imjoy.io/)

# Task manager

!> In this documentation, we provide a **dashboard** to define tasks, and **python code** to upload data to our server. This is for **demo purposes only**. The ImJoy team can access these data, and reserves the right to delete them at any moment. If you want to use the cloud annotator in your own projects, you will need to setup the task management server, as well as the data storage server (see here, TODO).

## Role

TODO

## Tasks

### Defining and modifying tasks

Tasks can be defined and modified via a dedicated ImJoy plugin, the Task-Dashboard. Tasks will be
stored on a task management server.

As a demo (see disclaimer above) for a dashboard click [**here**](https://imjoy.io/#/app?w=cloud-annotation&plugin=imjoy-team/imjoy-cloud-annotation:Task-Dashboard@stable&upgrade=1).

To define a new task or modify an existing task, follow these steps:

1. **Installation**. Clicking on this link, will open ImJoy in your browser and you will be asked to install the dashboard plugin. After confirmation, the plugin will show up in the plugin list on the left side of the ImJoy interface. You can run the plugin by pressing on its name.
2. **Login**. When opening the task manager for the first time, you will need to login (handled by   [https://auth0.com/](https://auth0.com/), so we don't have access to your passwords). You can either create an account, or use your existing GitHub or Google creditiens).

    ![task-dashboard-login](assets/task-dashboard-login.jpg ':size=200')
3. **Dashboard**. After the login, the dashboard will be shown.

   - `+ New Task`: create a new task.
   - Dropdown menu: lists all available tasks on the task server.
   - `... More`:
       - `Reload tasks`: will update the task list and their status.
       - `Connection Token`: display token for currently selected task, which is needed to upload data.
       - `Logout`: logout with current user.

    ![task-dashboard](assets/task-dashboard.jpg ':size=200')

When defining a task, the following **parameters** have to be defined:

Parameter               | Value      | Description
------------------------|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------
ID                      | string     | Unique identifier for a task.
Name                    | string     | Name of the task, e.g. will be used in the dropdown menu.
Type                    | string     | Type of task, e.g. `annotation`
Description             | string     | Longer description of the task.
Allow User upload       | True/False | Can user also upload their own data?
Input files             | list       | List of all input files, e.g. images, that should be displayed but won't be modified.
Target files            | list       | List of all target files, i.e. files that will be modified upon user intervention. For segmentation, this will be the segmentation results (see below).
Sampling Method         | choise     | How the samples are selected `sequential` or `random`.
User per sample | number | how many users can open a sample at the same time.
Minimal completion time (s) | number | Minimal time before a user can request a new sample.
Task visibility         | choice     | `public`: can be seen by all users, except users on the `blacklist` (email addresses). `protected`: task can be seen only by users listed in `whitelist` (email addresses).
Sample visibility       | choice     | `open`: all samples can be openly accessed,`protected`: users can only see 1 assigned sample at a time, not allowed to jump too any sample for annotation.
Sample Status File Name | string     | Name of file that will be created once a sample has been annotated by a user.
Expires in (s) | number | Duration after which a file will be released when being open by a user and not be resubmitted. 
client config | string | Configuration for the client (Kaibu). The proposed default creates a vector layer for polygon annotation.

### Public vs private tasks

An important aspects is privacy. Both the annotation tools and the Dashboard require a login, so 
differentiated access policies can be put into place

- A given task is **always accessible** for the user who created it and the 
adminstrators of the AI server.
- The `Task visibility` allows to **determine who else can see the task**. 
  - `public` means that everybody can access a task, except users being blacklisted.
  - `protected` means that only users listed on the `whitelist` can access the task. 

### Completing a task

In the task definition, a file-name is specified (`Sample Status File Name`), which is created once a sample has been annotated, e.g. __inspected_info.json. The presence of this file is considered as an indicator that the file has been inspected, and the sample is marked as complete.

## Data

### Data organization

We require a specific data organization.

1. Each sample, e.g. an image of one field of view, is stored in a separate folder, with a unique folder name.
2. The files in the folder names carry the same names across sample folders, e.g. a DAPI image will always be called ‘dapi.png’.

For instance, below the folder structure with two samples from the example data is shown:

``` bash
├─ demo_nuclei_annotation/
│  ├─ sample_1                          # Sample folder
│  │  ├─ dapi.png
│  │  ├─ annotation.json
│  ├─ sample_2                          # Sample folder
│  │  ├─ dapi.png
│  │  ├─ annotation.json
...
```

### Compatible file formats

Data inspection is done with customized [Kaibu plugins for ImJoy](https://kaibu.org/#/app). Kaibu can read

- **Images**: preferably 8bit png; mono-color, or RGB.
- **Vector annotations** stored as [GeoJson files](https://geojson.org/)

### Convert label images to GeoJson

In image segmentation results are usually provided as label images, where each segmented object is a filled polygon with a unique pixel value. While these images could be directly shown in Kaibu, no modification could be done by the user. However, such modification might be important to create a new training set.

In order to permit the user to modify these results, e.g. delete object(s) or add a new one, the images have to be converted into a GeoJson file.

We provide some Python code, showing how to convert label images for a nuclear segmentation to json files. This code also reorganizes and renames the data according to the above defined requirements (`utils\imjoy-ai-server-prepare-dataset.py`).

You can download some **test data** [here](https://www.dropbox.com/sh/hkr7xmpp9y5movz/AAAzHhbd-BhxNoA-1ZBQgviya?dl=0), with two folders:

1. Folder `segmentation-results`: contains the dapi images and the segmentation results as label images.
2. Folder `segmentation-annotation`: contains the reorganized data with the segmentation results stored as geojson files.

### Upload data

Once data is prepared, and a new task is created, a Python script (`utils\imjoy-ai-server-upload-dataset.py`) can be used to upload the data to the S3 data server:

1. Use the `AIServerDashboard` (see above) to create a new task, you will be asked to provide a task id.
2. Once the task is created, obtain a connection token by clicking on the `Info` button.
3. Use the `token` and `task id` in the Python script to upload an entire dataset.

## Annotation plugin

As a demo (see disclaimer above) for annotation plugin see [**here**](https://imjoy.io/#/app?w=cloud-annotation&plugin=imjoy-team/imjoy-cloud-annotation:Nuclei-Cloud-Annotator@stable&upgrade=1).

This plugin provides all major features for multi-user annotation. In order to point it to a new annotation task, only two lines have to be changed:

``` javascript
const TASK_ID = 'demo-annotate-nuclei'
const BASE_URL = 'https://api.imjoy.io'
```

- `TASK_ID`: ID of the task
- `BASE_URL` is the URL of the task management server, here our demo server.

Kaibu permits further customization of this plugin, more information can be found in the dedicated section for the client developer. 

### Distributing of annotation plugins

ImJoy provides the possiblity to distribute a plugin wiht an URL. This URL references the actual plugin that 
should be installed, and further optional information detailing how the plugin should be installed. 

As an example the URL shown below is for the Nuclei-Annotation plugin

``` url
https://imjoy.io/#/app?w=cloud-annotation&plugin=imjoy-team/imjoy-cloud-annotation:Nuclei-Cloud-Annotator@stable&upgrade=1
```

ImJoy provides a lot of flexibility for how to host your plugin codes. 

1. **Any website**, including GitHub, Gist or Dropbox. For testing, we recommend using GitHub Gist.
2. **ImJoy plugin repository**. Any GitHub respository can act as a plugin repository, and requires only the addition of one file.  provides the most flexibility and is our recommended way when you have multipled plugins.

A **detailed description** for how to construct this urls and where plugin code can be hosted, can be found in the ImJoy documentation [**here**](https://imjoy.io/docs/#/development?id=generating-a-plugin-url-for-sharing)

## Retrieving data

The data belonging to a task can also be retrieved from the storage server with the provided Python script (`utils\imjoy-ai-server-download-dataset.py`).

This script will download the entire data set to a user-specified folder. The data is organized as the uploaded data, 
with one important change. The target files will be in stored in a dedicated folder in each sample folder named `target_files_vi`, 
where `i` is a version number. `v0` is the originally provided target file, e.g. the original segmentation files, subsequent versions, e.g. `v1`, `v2` are created if for this sample a new annotation was submitted. 

An status file (`status_file.json`) will be created in each sample folder providing detailed information about each version (who annotated it, when, ...). This allows to determine which user(s) annotated the samples.

Some important considerations

- The **version numbers are chronological** and not by user. So if different users work on the same task, their annotations will not have the same version number for different samples. 
- A completed annotation of the **same sample by the same user** will results in two distinct versions.
