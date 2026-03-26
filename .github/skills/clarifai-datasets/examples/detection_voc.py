# Detection DataLoader - VOC XML format
# Source: github.com/Clarifai/examples/datasets/upload/image_detection/voc/dataset.py
#
# Data structure:
#   voc/
#   ├── dataset.py (this file)
#   ├── images/
#   │   ├── 2007_000464.jpg
#   │   └── 2008_003182.jpg
#   └── annotations/
#       ├── 2007_000464.xml
#       └── 2008_003182.xml

import os
import xml.etree.ElementTree as ET

from clarifai.datasets.upload.base import ClarifaiDataLoader
from clarifai.datasets.upload.features import VisualDetectionFeatures


class VOCDetectionDataLoader(ClarifaiDataLoader):
    """PASCAL VOC 2012 Image Detection Dataset."""

    voc_concepts = [
        'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat',
        'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person',
        'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor'
    ]

    def __init__(self, split: str = "train"):
        self.split = split
        self.image_dir = {"train": os.path.join(os.path.dirname(__file__), "images")}
        self.annotations_dir = {"train": os.path.join(os.path.dirname(__file__), "annotations")}
        self.annotations = []
        self.load_data()

    @property
    def task(self):
        return "visual_detection"

    def load_data(self):
        all_imgs = os.listdir(self.image_dir[self.split])
        img_ids = [img_filename.split('.')[0] for img_filename in all_imgs]

        for _id in img_ids:
            annot_path = os.path.join(self.annotations_dir[self.split], _id + ".xml")
            if not os.path.exists(annot_path):
                continue

            root = ET.parse(annot_path).getroot()

            annots = []
            class_names = []
            for obj in root.iter('object'):
                concept = obj.find('name').text.strip().lower()
                if concept not in self.voc_concepts:
                    continue

                xml_box = obj.find('bndbox')
                width = float(root.find('size').find('width').text)
                height = float(root.find('size').find('height').text)

                # CRITICAL: VOC uses -1 adjustment, normalize to 0-1 range
                x_min = max(min((float(xml_box.find('xmin').text) - 1) / width, 1.0), 0.0)
                y_min = max(min((float(xml_box.find('ymin').text) - 1) / height, 1.0), 0.0)
                x_max = max(min((float(xml_box.find('xmax').text) - 1) / width, 1.0), 0.0)
                y_max = max(min((float(xml_box.find('ymax').text) - 1) / height, 1.0), 0.0)

                if (x_min >= x_max) or (y_min >= y_max):
                    continue

                annots.append([x_min, y_min, x_max, y_max])
                class_names.append(concept)

            assert len(class_names) == len(annots), \
                f"Num classes must match num bbox annotations. Found {len(class_names)} classes and {len(annots)} bboxes."

            self.annotations.append({
                "image_id": _id,
                "image_path": os.path.join(self.image_dir[self.split], _id + ".jpg"),
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
