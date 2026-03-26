---
name: clarifai-datasets
description: Upload and manage datasets on Clarifai platform. Use when the user wants to upload image datasets with annotations (classification, detection, segmentation), convert data formats (COCO, VOC, YOLO), create custom DataLoader classes, or manage dataset inputs. Covers load_module_dataloader pattern, Feature classes, and dataset operations.
---

# Dataset Upload & Management

> **IMPORTANT:** For SDK methods and CLI commands and code generation, first scan [../clarifai-cli/references/sdk-cli-reference.md](../clarifai-cli/references/sdk-cli-reference.md)

Upload annotated datasets to Clarifai platform for training and inference.

## Decision Tree

**ALWAYS check this decision tree FIRST before generating code:**

```
Does user have existing dataset.py?
├── YES → Generate upload_script.py only (ONE file)
└── NO → Generate dataset.py + upload_script.py (TWO files)
         └── dataset.py MUST be placed IN the data directory
```

## Feature Classes Quick Reference

| Task | Feature Class | task Property |
|------|---------------|---------------|
| Classification | `VisualClassificationFeatures` | `visual_classification` |
| Detection | `VisualDetectionFeatures` | `visual_detection` |
| Segmentation | `VisualSegmentationFeatures` | `visual_segmentation` |

## Critical Rules

1. **Bounding boxes must be normalized to 0-1 range** - Divide pixel coordinates by image width/height
2. **VOC format uses -1 adjustment** - `(coord - 1) / dimension` per VOC convention
3. **YOLO format is center-based** - Convert `(x_center, y_center, w, h)` to `(left, top, right, bottom)`
4. **NEVER use `upload_from_file()` with `bboxes` parameter** - Method signature doesn't exist
5. **Dataset.py must be IN the data directory** - `load_module_dataloader()` looks for it there

## Upload Methods

| Method | When to Use |
|--------|-------------|
| `load_module_dataloader()` | Custom DataLoader class (RECOMMENDED) |
| `upload_from_folder()` | Simple classification from folders |
| `upload_from_csv()` | Data in CSV format |

### Quick Upload Pattern

```python
from clarifai.client.dataset import Dataset
from clarifai.datasets.upload.utils import load_module_dataloader

dataset = Dataset(user_id="user_id", app_id="app_id", dataset_id="dataset_id")
dataloader = load_module_dataloader('./path/to/data_dir')  # Contains dataset.py
dataset.upload_dataset(dataloader=dataloader, get_upload_status=True, log_warnings=True)
```

### Folder Upload (Simple Classification)

```python
# Folder structure: images/class1/*.jpg, images/class2/*.jpg
dataset.upload_from_folder(folder_path='images/', input_type='image', labels=True)
```

### CSV Upload

```python
dataset.upload_from_csv(csv_path='data.csv', input_type='text', csv_type='raw', labels=True)
# csv_type options: 'raw', 'url', 'file_path'
```

**CSV columns:** `inputid`, `input`, `concepts`, `metadata`, `geopoints`

## DataLoader Requirements

Every custom DataLoader must:
1. Extend `ClarifaiDataLoader`
2. Implement `@property def task(self)` returning: `"visual_classification"`, `"visual_detection"`, or `"visual_segmentation"`
3. Implement `__len__(self)` returning total items
4. Implement `__getitem__(self, idx)` returning the appropriate Feature object

## Dataset Management

```python
# List inputs
inputs = list(dataset.list_inputs())

# Delete inputs
from clarifai.client.input import Inputs
input_obj = Inputs(user_id="user_id", app_id="app_id")
input_obj.delete_inputs(inputs)

# Versions
versions = list(dataset.list_versions())
new_version = dataset.create_version()

# Export
dataset.export(save_path='output.zip')

# Retry failed uploads
dataset.retry_upload_from_logs(dataloader=dataloader, log_file_path='./Dataset_Upload.log')
```

## Export Format

**CRITICAL: Clarifai exports use camelCase keys**

```json
{
  "regionInfo": {
    "boundingBox": {
      "topRow": 0.194,
      "bottomRow": 0.853,
      "leftCol": 0.0,
      "rightCol": 0.892
    }
  },
  "data": {
    "concepts": [{"id": "class-name", "name": "class-name", "value": 1.0}]
  }
}
```

## Format Conversion (Export)

```python
# pip install clarifai-datautils
from clarifai_datautils import ImageAnnotations

# Import Clarifai format
clarifai_dataset = ImageAnnotations.import_from(path='./exported_data', format='clarifai')

# Export to COCO
clarifai_dataset.export_to(path='./coco_output', format='coco_detection', save_images=True)

# Export to YOLO
clarifai_dataset.export_to(path='./yolo_output', format='yolo', save_images=True)
```

## Extended Search

For more examples and edge cases, search the official examples codebase:
- **Dataset upload examples**: https://github.com/Clarifai/examples/tree/main/datasets/upload
- **Dataset export examples**: https://github.com/Clarifai/examples/tree/main/datasets/export
- **SDK docs**: https://docs.clarifai.com/data/datasets/

## References

- DataLoader patterns: [references/dataloader-patterns.md](references/dataloader-patterns.md)

## Examples

Working examples from official Clarifai examples repo:
- Classification (CSV): [examples/classification_cifar10.py](examples/classification_cifar10.py)
- Classification (folder): [examples/classification_food101.py](examples/classification_food101.py)
- Detection (VOC XML): [examples/detection_voc.py](examples/detection_voc.py)
- Detection (YOLO TXT): [examples/detection_yolo.py](examples/detection_yolo.py)
- Segmentation (COCO): [examples/segmentation_coco.py](examples/segmentation_coco.py)
- Upload script: [examples/upload_script.py](examples/upload_script.py)
