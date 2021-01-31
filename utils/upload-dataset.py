# %% Upload data to ImJoy S3 annotation server
#  DISCLAIMER: FOR DEMO PURPOSES ONLY
#   The ImJoy team has full access to these data, and reservers
#   all rights to delete data as any moment.
#
#  Data is uploaded with html requests.
#   How to use requests: https://requests.readthedocs.io/en/master/user/quickstart/


# %% Imports
import os
import requests


# %% Specify the task and data directory

BASE_URL = "https://ai.pasteur.fr"

# Get the token from the AIServerDashboard plugin
#  * https://imjoy.io/#/app?w=cloud-annotation&plugin=imjoy-team/imjoy-cloud-annotation:Task-Dashboard@stable&upgrade=1
#  * Login as an admin user and click the info button to copy the token string
TOKEN = "PASTE YOUR TOKEN HERE"

# Folder contaning the data to be uploaded (organized according to our specifications)
#  For the demo data, this is the folder "segmentation-annotation"
DATASET_DIR = "my-dataset"

# This is the task which you want to upload new samples to
TASK_ID = "my-task"


# %% Upload data to the server

# listing tasks
response = requests.get(
    BASE_URL + "/tasks", headers={"Authorization": f"Bearer {TOKEN}"}
)
response_obj = response.json()
assert (
    response_obj["success"] == True
), f"Failed to requesting URL for upload, error: {response_obj['error']}"
tasks = response_obj["result"]


assert (
    TASK_ID in tasks
), f"Task {TASK_ID} not found, must be one of: {list(tasks.keys())}"


# upload a sample to the task
count = 0
all_samples = os.listdir(DATASET_DIR)
for sample_id in all_samples:
    if not os.path.isdir(os.path.join(DATASET_DIR, sample_id)):
        continue
    count += 1
    print(f"===> ({count}/{len(all_samples)}) Uploading {sample_id} ...")
    response = requests.get(
        BASE_URL + f"/task/{TASK_ID}/sample/{sample_id}/upload?exist_ok=1",
        headers={"Authorization": f"Bearer {TOKEN}"},
    )
    response_obj = response.json()
    assert (
        response_obj["success"] == True
    ), f"Failed to requesting URL for upload, error: {response_obj.get('detail') or response_obj['error']}"
    result = response_obj["result"]

    # upload input files
    for file_name in result["input_files"]:
        input_file = os.path.join(DATASET_DIR, sample_id, file_name)
        upload_url = result["input_files"][file_name]
        # read the file content here
        content = open(input_file, "rb")
        response = requests.put(upload_url, data=content)
        assert (
            response.status_code == 200
        ), f"failed to upload file: {file_name}, {response.reason}: {response.text}"

    # upload target files
    for file_name in result["target_files"]:
        target_file = os.path.join(DATASET_DIR, sample_id, file_name)
        # allow skipping the upload if not exists
        if not os.path.exists(target_file):
            continue
        upload_url = result["target_files"][file_name]
        # read the file content here
        content = open(target_file, "rb")
        response = requests.put(upload_url, data=content)
        assert (
            response.status_code == 200
        ), f"failed to upload file: {file_name}, {response.reason}: {response.text}"

    # now refresh this sample
    response = requests.post(
        BASE_URL + f"/task/{TASK_ID}/sample/{sample_id}/refresh",
        headers={"Authorization": f"Bearer {TOKEN}"},
    )
    response_obj = response.json()
    assert (
        response_obj["success"] == True
    ), f"Failed to enable sample, error: {response_obj.get('detail') or response_obj['error']}"

# %%
