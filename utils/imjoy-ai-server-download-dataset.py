# %% Download data from ImJoy AI Server
#
#  Data is downloaded with html requests.
#   How to use requests: https://requests.readthedocs.io/en/master/user/quickstart/


# %% Imports
import os
import requests


# %% Specify the task and data directory

BASE_URL = "https://api.imjoy.io"

# Get the token from the AIServerDashboard plugin
#  * https://imjoy.io/#/app?w=cloud-annotation&plugin=imjoy-team/imjoy-cloud-annotation:Task-Dashboard@stable&upgrade=1
#  * Login as an admin user and click the "Connection Token" menu item to copy the token string
TOKEN = "PASTE YOUR TOKEN HERE"

# Folder where data should be stored
SAVE_DIR = "PASTE-PATH-TO-SAVE-DATA"

# This is the task which which you want to download
TASK_ID = "demo-annotate-nuclei"


# %% Download dataset from the server

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

# Create folder to save data if does not exist
os.makedirs(SAVE_DIR, exist_ok=True)

# downloading samples
count = 0
response = requests.get(
    BASE_URL + f"/task/{TASK_ID}/all", headers={"Authorization": f"Bearer {TOKEN}"}
)

response_obj = response.json()
assert response_obj["success"] == True, "Failed to get samples"

all_samples = response_obj["result"]
chunk_size = 1024 * 100

for sample_id in all_samples:
    count += 1
    print(f"===> ({count}/{len(all_samples)}) Downloading {sample_id} ...")
    response = requests.get(
        BASE_URL + f"/task/{TASK_ID}/sample/{sample_id}?target_version=all",
        headers={"Authorization": f"Bearer {TOKEN}"},
    )
    response_obj = response.json()
    if response.status_code != 200:
        print(f"Failed to requesting URL for download, error: {response_obj.get('detail') or response_obj['error']}")
        continue
    if not response_obj["success"]:
        print("Failed to download "+response_obj["error"])
        continue
    result = response_obj["result"]
    if not result.get("input_files"):
        continue
    os.makedirs(os.path.join(SAVE_DIR, sample_id), exist_ok=True)
    print(f'    Saving to {os.path.join(SAVE_DIR, sample_id)}')
    
    # Download input files
    for file_name in result["input_files"]:
        input_file = os.path.join(SAVE_DIR, sample_id, file_name)
        download_url = result["input_files"][file_name]
        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            with open(input_file, "wb") as fd:
                for chunk in response.iter_content(chunk_size):
                    fd.write(chunk)
        else:
            print(f"failed to download file: {file_name}, {response.reason}: {response.text}")
        
    # Download target files
    for file_name in result["target_files"]:
        target_versions = result["target_files"][file_name]
        if len(target_versions) <= 0:
            continue
        for version in target_versions:
            os.makedirs(os.path.join(SAVE_DIR, sample_id, version), exist_ok=True)
            target_file = os.path.join(SAVE_DIR, sample_id, version, file_name)
            download_url = target_versions[version]
            response = requests.get(download_url, stream=True)
            if response.status_code == 200:
                with open(target_file, "wb") as fd:
                    for chunk in response.iter_content(chunk_size):
                        fd.write(chunk)
            else:
                print(f"Failed to download file: {file_name}, {response.reason}: {response.text}")
            

# %%
