# %% Upload data to ImJoy S3 annotation server and perform conversion
#  DISCLAIMER: FOR DEMO PURPOSES ONLY
#   The ImJoy team has full access to these data, and reservers
#   all rights to delete data as any moment.
#
#  Data is uploaded with html requests.
#   How to use requests: https://requests.readthedocs.io/en/master/user/quickstart/


# %% Imports
import os
import time
import requests


# %% Specify the task and data directory

BASE_URL = "https://ai.pasteur.fr"

# Get the token from the AIServerDashboard plugin
#  * https://imjoy.io/#/app?w=cloud-annotation&plugin=imjoy-team/imjoy-cloud-annotation:Task-Dashboard@stable&upgrade=1
#  * Login as an admin user and click the info button to copy the token string
TOKEN = "PASTE THE TOKEN HERE"


# This is the dataset_id which you want to upload new samples to
# You can create a new task and a dataset with the same id will be created
# In the task, please add `["image.ome.tif", "image.ome.tif_offsets.json"]` as `input_files`
# and you can leave `target_files` as []
DATASET_ID = "my-dataset-id"

# Define the folder with data
# As an example, you can download and extract this sample image in dm3 format: https://samples.scif.io/dnasample1.zip
DATASET_DIR = "./data"
UPLOAD_FILES = ["image.dm3"]

# convert image.dm3 to image.ome.tif
CONVERT_FILES = {"image.dm3": "image.ome.tif"}

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
    DATASET_ID in tasks
), f"Task {DATASET_ID} not found, must be one of: {list(tasks.keys())}"


# %% download example file
os.makedirs(os.path.join(DATASET_DIR, 'dnasample1'), exist_ok=True)
r = requests.get("https://samples.scif.io/dnasample1.zip", allow_redirects=True)
open(os.path.join(DATASET_DIR, 'dnasample1.zip'), 'wb').write(r.content)
import zipfile
with zipfile.ZipFile(os.path.join(DATASET_DIR, 'dnasample1.zip'), 'r') as zip_ref:
    zip_ref.extractall(DATASET_DIR)
os.rename(os.path.join(DATASET_DIR, 'dnasample1.dm3'), os.path.join(DATASET_DIR, 'dnasample1', 'image.dm3'))

# upload a sample to the task
count = 0
all_samples = os.listdir(DATASET_DIR)
for sample_id in all_samples:
    if not os.path.isdir(os.path.join(DATASET_DIR, sample_id)):
        continue
    count += 1
    print(f"===> ({count}/{len(all_samples)}) Uploading {sample_id} ...")
    response = requests.get(
        BASE_URL + f"/dataset/{DATASET_ID}/sample/{sample_id}/upload?exist_ok=1",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json=UPLOAD_FILES
    )
    response_obj = response.json()
    assert (
        response_obj["success"] == True
    ), f"Failed to requesting URL for upload, error: {response_obj.get('detail') or response_obj['error']}"
    result = response_obj["result"]
    # upload files
    for file_name in UPLOAD_FILES:
        input_file = os.path.join(DATASET_DIR, sample_id, file_name)
        upload_url = result["files"][file_name]

        # read the file content here
        content = open(input_file, "rb")
        response = requests.put(upload_url, data=content)
        assert (
            response.status_code == 200
        ), f"failed to upload file: {file_name}, {response.reason}: {response.text}"

        if file_name not in CONVERT_FILES:
            continue

        # convert format
        response = requests.post(
            BASE_URL + f"/dataset/{DATASET_ID}/sample/{sample_id}/convert",
            headers={"Authorization": f"Bearer {TOKEN}"},
            json={input_file: {"format": "ome-tiff", "output_file": CONVERT_FILES[input_file]} for input_file in result["files"]}
        )
        response_obj = response.json()
        assert (
            response_obj["success"] == True
        ), f"Failed to convert sample, error: {response_obj.get('detail') or response_obj['error']}"
        session_id = response_obj["result"]["session_id"]
        # check conversion status
        while True:
            response = requests.get(
                BASE_URL + f"/conversion/status/{session_id}",
                headers={"Authorization": f"Bearer {TOKEN}"},
            )
            response_obj = response.json()
            assert (
                response_obj.get("success") == True
            ), f"Failed to get conversion status, error: {response_obj.get('detail') or response_obj['error']}"
            result = response_obj["result"]
            print(result["status"])
            if result['completed']:
                break
            time.sleep(1)
        
    
    # now refresh this sample
    response = requests.post(
        BASE_URL + f"/dataset/{DATASET_ID}/sample/{sample_id}/refresh",
        headers={"Authorization": f"Bearer {TOKEN}"},
    )
    response_obj = response.json()
    assert (
        response_obj["success"] == True
    ), f"Failed to enable sample, error: {response_obj.get('detail') or response_obj['error']}"

    response = requests.get(
        BASE_URL + f"/dataset/{DATASET_ID}/sample/{sample_id}",
        headers={"Authorization": f"Bearer {TOKEN}"},
    )
    response_obj = response.json()
    assert (
        response_obj["success"] == True
    ), f"Failed to enable sample, error: {response_obj.get('detail') or response_obj['error']}"
    for file in response_obj["result"]["files"]:
        url = response_obj["result"]["files"][file]
        print(f"{file}: {url}")
