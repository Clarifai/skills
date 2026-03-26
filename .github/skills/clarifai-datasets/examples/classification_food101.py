# Classification DataLoader - Folder-based (Food101 style)
# Source: github.com/Clarifai/examples/datasets/upload/image_classification/food-101/dataset.py
#
# Data structure:
#   food-101/
#   ├── dataset.py (this file)
#   └── images/
#       ├── pizza/
#       │   ├── img1.jpg
#       │   └── img2.jpg
#       └── burger/
#           ├── img3.jpg
#           └── img4.jpg

import os

from clarifai.datasets.upload.base import ClarifaiDataLoader
from clarifai.datasets.upload.features import VisualClassificationFeatures


class Food101DataLoader(ClarifaiDataLoader):
    """Food-101 Image Classification Dataset - folder-based."""

    def __init__(self, split: str = "train"):
        """Initialize dataset params.
        Args:
            split: "train" or "test"
        """
        self.split = split
        self.image_dir = {"train": os.path.join(os.path.dirname(__file__), "images")}
        self.load_data()

    @property
    def task(self):
        return "visual_classification"

    def load_data(self):
        """Load data for the food-101 dataset."""
        self.data = []
        class_names = os.listdir(self.image_dir[self.split])
        for class_name in class_names:
            class_dir = os.path.join(self.image_dir[self.split], class_name)
            if not os.path.isdir(class_dir):
                continue
            for image in os.listdir(class_dir):
                if image.endswith(('.jpg', '.jpeg', '.png')):
                    image_path = os.path.join(class_dir, image)
                    self.data.append({
                        "image_path": image_path,
                        "class_name": class_name,
                    })

    def __getitem__(self, idx):
        data_item = self.data[idx]
        image_path = data_item["image_path"]
        class_name = data_item["class_name"]
        return VisualClassificationFeatures(
            image_path=image_path,
            labels=[class_name],
            id=os.path.basename(image_path).split(".")[0]
        )

    def __len__(self):
        return len(self.data)
