# DataLoader Patterns Reference

Comprehensive patterns for creating custom ClarifaiDataLoader classes.

## Available Feature Classes

```python
from clarifai.datasets.upload.base import ClarifaiDataLoader
from clarifai.datasets.upload.features import (
    VisualClassificationFeatures,  # Image classification
    VisualDetectionFeatures,       # Object detection with bboxes
    VisualSegmentationFeatures,    # Image segmentation with polygons
)
```

## DataLoader Interface

Every custom DataLoader must implement:

```python
class MyDataLoader(ClarifaiDataLoader):
    def __init__(self, ...):
        # Initialize paths, load data
        pass

    @property
    def task(self):
        # Return: "visual_classification", "visual_detection", or "visual_segmentation"
        return "visual_classification"

    def __len__(self):
        # Return total number of items
        return len(self.data)

    def __getitem__(self, idx):
        # Return appropriate Feature object
        return VisualClassificationFeatures(...)
```

## Classification Patterns

### CSV-Based (Cifar10 style)

```python
class CSVClassificationDataLoader(ClarifaiDataLoader):
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.data = self.load_data()

    @property
    def task(self):
        return "visual_classification"

    def load_data(self):
        data = []
        with open(self.csv_path) as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            for row in reader:
                data.append((row[0], row[1]))  # image_path, label
        return data

    def __getitem__(self, idx):
        image_path, label = self.data[idx]
        return VisualClassificationFeatures(
            image_path=image_path,
            labels=[label],
            id=os.path.basename(image_path).split(".")[0]
        )

    def __len__(self):
        return len(self.data)
```

### Folder-Based (Food101 style)

```python
class FolderClassificationDataLoader(ClarifaiDataLoader):
    def __init__(self, image_dir: str):
        self.image_dir = image_dir
        self.data = []
        self.load_data()

    @property
    def task(self):
        return "visual_classification"

    def load_data(self):
        for class_name in os.listdir(self.image_dir):
            class_dir = os.path.join(self.image_dir, class_name)
            if not os.path.isdir(class_dir):
                continue
            for image in os.listdir(class_dir):
                if image.endswith(('.jpg', '.jpeg', '.png')):
                    self.data.append({
                        "image_path": os.path.join(class_dir, image),
                        "class_name": class_name,
                    })

    def __getitem__(self, idx):
        item = self.data[idx]
        return VisualClassificationFeatures(
            image_path=item["image_path"],
            labels=[item["class_name"]],
            id=os.path.basename(item["image_path"]).split(".")[0]
        )

    def __len__(self):
        return len(self.data)
```

## Detection Patterns

### VOC XML Format

**Key: Use -1 adjustment per VOC convention when normalizing**

```python
class VOCDetectionDataLoader(ClarifaiDataLoader):
    def __init__(self, image_dir: str, annotations_dir: str):
        self.image_dir = image_dir
        self.annotations_dir = annotations_dir
        self.annotations = []
        self.load_data()

    @property
    def task(self):
        return "visual_detection"

    def load_data(self):
        for img_file in os.listdir(self.image_dir):
            if not img_file.endswith(('.jpg', '.jpeg', '.png')):
                continue
            img_id = os.path.splitext(img_file)[0]
            annot_path = os.path.join(self.annotations_dir, f"{img_id}.xml")
            if not os.path.exists(annot_path):
                continue

            root = ET.parse(annot_path).getroot()
            width = float(root.find('size/width').text)
            height = float(root.find('size/height').text)

            annots = []
            class_names = []
            for obj in root.iter('object'):
                concept = obj.find('name').text.strip().lower()
                bbox = obj.find('bndbox')

                # CRITICAL: VOC uses -1 adjustment
                x_min = max(min((float(bbox.find('xmin').text) - 1) / width, 1.0), 0.0)
                y_min = max(min((float(bbox.find('ymin').text) - 1) / height, 1.0), 0.0)
                x_max = max(min((float(bbox.find('xmax').text) - 1) / width, 1.0), 0.0)
                y_max = max(min((float(bbox.find('ymax').text) - 1) / height, 1.0), 0.0)

                if x_min < x_max and y_min < y_max:
                    annots.append([x_min, y_min, x_max, y_max])
                    class_names.append(concept)

            self.annotations.append({
                "image_id": img_id,
                "image_path": os.path.join(self.image_dir, img_file),
                "class_names": class_names,
                "annots": annots
            })

    def __getitem__(self, idx):
        annot = self.annotations[idx]
        return VisualDetectionFeatures(
            annot["image_path"],
            annot["class_names"],
            annot["annots"],
            id=annot["image_id"]
        )

    def __len__(self):
        return len(self.annotations)
```

### YOLO TXT Format

**Key: YOLO uses center-based coordinates, convert to corner-based**

```python
class YOLODetectionDataLoader(ClarifaiDataLoader):
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.data = []
        self.load_data()

    @property
    def task(self):
        return "visual_detection"

    def load_data(self):
        for subdir in os.listdir(self.root_dir):
            subdir_path = os.path.join(self.root_dir, subdir)
            if os.path.isdir(subdir_path):
                for filename in os.listdir(subdir_path):
                    if filename.endswith(('.jpg', '.png')):
                        image_path = os.path.join(subdir_path, filename)
                        annot_path = os.path.join(subdir_path, os.path.splitext(filename)[0] + '.txt')
                        if os.path.exists(annot_path):
                            self.data.append((image_path, annot_path))

    def __getitem__(self, idx):
        image_path, annot_path = self.data[idx]
        annots = []
        concept_ids = []

        with open(annot_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) != 5:
                    continue
                class_id, x_center, y_center, width, height = map(float, parts)

                # Convert YOLO (center, w, h) to Clarifai (left, top, right, bottom)
                left = max(0, x_center - width / 2)
                top = max(0, y_center - height / 2)
                right = min(1, x_center + width / 2)
                bottom = min(1, y_center + height / 2)

                if left < right and top < bottom:
                    annots.append([left, top, right, bottom])
                    concept_ids.append(str(int(class_id)))

        # Clean filename for ID
        image_filename = os.path.basename(image_path)
        id_str = os.path.splitext(image_filename)[0].replace(' ', '_')

        return VisualDetectionFeatures(image_path, concept_ids, annots, id=id_str)

    def __len__(self):
        return len(self.data)
```

## Segmentation Patterns

### COCO JSON Format

**Requirements:** `pip install pycocotools opencv-python numpy`

```python
class COCOSegmentationDataLoader(ClarifaiDataLoader):
    def __init__(self, image_dir: str, annotations_file: str):
        self.image_dir = image_dir
        self.annotations_file = annotations_file
        self.load_data()

    @property
    def task(self):
        return "visual_segmentation"

    def load_data(self):
        self.coco = COCO(self.annotations_file)
        categories = self.coco.loadCats(self.coco.getCatIds())
        self.cat_id_map = {cat["id"]: cat["name"] for cat in categories}
        self.cat_img_ids = {}
        for cat_id in self.cat_id_map.keys():
            self.cat_img_ids[cat_id] = self.coco.getImgIds(catIds=[cat_id])

        img_ids = []
        for ids in self.cat_img_ids.values():
            img_ids.extend(ids)

        image_info = self.coco.loadImgs(img_ids)
        self.image_filenames = {img_id: info['file_name'] for info, img_id in zip(image_info, img_ids)}
        self.img_ids = list(set(img_ids))

    def __getitem__(self, idx):
        _id = self.img_ids[idx]
        annots = []
        class_names = []
        labels = [i for i in filter(lambda x: _id in self.cat_img_ids[x], self.cat_img_ids)]
        image_path = os.path.join(self.image_dir, self.image_filenames[_id])

        image_height, image_width = cv2.imread(image_path).shape[:2]

        for cat_id in labels:
            annot_ids = self.coco.getAnnIds(imgIds=_id, catIds=[cat_id])
            if len(annot_ids) == 0:
                continue

            img_annotations = self.coco.loadAnns(annot_ids)
            for ann in img_annotations:
                if isinstance(ann['segmentation'], list):
                    # Polygon format
                    for seg in ann['segmentation']:
                        poly = np.array(seg).reshape((len(seg) // 2, 2))
                        poly[:, 0] = poly[:, 0] / image_width  # Normalize x
                        poly[:, 1] = poly[:, 1] / image_height  # Normalize y
                        annots.append(poly.tolist())
                        class_names.append(self.cat_id_map[cat_id])
                else:
                    # RLE format - convert to polygon
                    if isinstance(ann['segmentation']['counts'], list):
                        rle = maskUtils.frPyObjects([ann['segmentation']], image_height, image_width)
                    else:
                        rle = ann['segmentation']
                    mask = maskUtils.decode(rle)
                    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    polygons = [cont.astype(float).flatten().tolist() for cont in contours if cont.size >= 6]
                    if polygons:
                        polygons_flat = reduce(lambda x, y: x + y, polygons)
                        poly = np.array(polygons_flat).reshape((len(polygons_flat) // 2, 2))
                        poly[:, 0] = poly[:, 0] / image_width
                        poly[:, 1] = poly[:, 1] / image_height
                        annots.append(poly.tolist())
                        class_names.append(self.cat_id_map[cat_id])
                    del mask, contours
                    gc.collect()

        return VisualSegmentationFeatures(
            image_path, class_names, annots, id=self.image_filenames[_id].split(".")[0]
        )

    def __len__(self):
        return len(self.img_ids)
```

## Upload Script Pattern

```python
import os
from clarifai.client.user import User
from clarifai.datasets.upload.utils import load_module_dataloader

# Configuration
DATA_PATH = "/path/to/your/data"  # Directory containing dataset.py
USER_ID = os.environ.get("CLARIFAI_USER_ID", "your_user_id")
APP_ID = "my-app"
DATASET_ID = "my-dataset"

# Create app and dataset
user = User(user_id=USER_ID)
app = user.create_app(app_id=APP_ID, base_workflow="Empty")
dataset = app.create_dataset(dataset_id=DATASET_ID)

# Load dataloader from data directory
dataloader = load_module_dataloader(DATA_PATH)

# Upload with status reporting
dataset.upload_dataset(dataloader=dataloader, get_upload_status=True, log_warnings=True)

print(f"Done! Dataset: https://clarifai.com/{USER_ID}/{APP_ID}/datasets/{DATASET_ID}")
```

## Using root_dir for External Data

For dataloaders that need a custom data path:

```python
dataloader = load_module_dataloader(
    './path/to/dataloader_module',
    root_dir='./path/to/actual/data'
)
```

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| Bounding boxes outside 0-1 range | Normalize: `coord / dimension` |
| VOC coordinates off by 1 | Use `(coord - 1) / dimension` |
| YOLO center vs corner | Convert: `left = x_center - width/2` |
| Invalid bbox (min >= max) | Skip or clamp invalid boxes |
| Missing annotation file | Check existence before parsing |
| Duplicate input IDs | Generate unique IDs from filename |
