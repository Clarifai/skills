# Upload Script Template
# Source: github.com/Clarifai/examples/datasets/upload/README.md
#
# This script uploads a dataset to Clarifai using a DataLoader.
# Place the DataLoader class (dataset.py) IN the data directory,
# then run this script from your working directory.

import os
from clarifai.client.user import User
from clarifai.datasets.upload.utils import load_module_dataloader

# ============================================================================
# Configuration - Update these values
# ============================================================================

DATA_PATH = "/path/to/your/data"  # Directory containing dataset.py
USER_ID = os.environ.get("CLARIFAI_USER_ID", "your_user_id")
APP_ID = "my-app"
DATASET_ID = "my-dataset"

# ============================================================================
# Create App and Dataset
# ============================================================================

user = User(user_id=USER_ID)

# Create app (or use existing)
try:
    app = user.create_app(app_id=APP_ID, base_workflow="Empty")
    print(f"Created app: {APP_ID}")
except Exception as e:
    app = user.app(app_id=APP_ID)
    print(f"Using existing app: {APP_ID}")

# Create dataset (or use existing)
try:
    dataset = app.create_dataset(dataset_id=DATASET_ID)
    print(f"Created dataset: {DATASET_ID}")
except Exception as e:
    dataset = app.dataset(dataset_id=DATASET_ID)
    print(f"Using existing dataset: {DATASET_ID}")

# ============================================================================
# Load DataLoader and Upload
# ============================================================================

# Load dataloader from data directory (finds dataset.py automatically)
dataloader = load_module_dataloader(DATA_PATH)
print(f"Loaded dataloader with {len(dataloader)} items")

# Upload with status reporting
# - get_upload_status=True: Shows upload summary
# - log_warnings=True: Logs failures to file for retry
dataset.upload_dataset(
    dataloader=dataloader,
    get_upload_status=True,
    log_warnings=True
)

print(f"\nDone! Dataset: https://clarifai.com/{USER_ID}/{APP_ID}/datasets/{DATASET_ID}")

# ============================================================================
# Optional: For YOLO with external data path, use root_dir parameter
# ============================================================================
#
# dataloader = load_module_dataloader(
#     './path/to/dataloader_module',
#     root_dir='/path/to/actual/data'
# )

# ============================================================================
# Optional: Retry failed uploads
# ============================================================================
#
# dataset.retry_upload_from_logs(
#     dataloader=dataloader,
#     log_file_path='./Dataset_Upload.log',
#     retry_duplicates=False,
#     log_warnings=True
# )
