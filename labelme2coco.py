"""
labelme格式转换成coco格式
"""
import os
import json
import glob
import numpy as np
from PIL import Image


def labelme_to_coco(labelme_dir, save_path):
    labelme_files = glob.glob(os.path.join(labelme_dir, "*.json"))
    images = []
    annotations = []
    categories = []

    # Mapping from LabelMe category names to COCO category IDs
    category_mapping = {}

    # Initialize category ID counter
    category_id = 1

    for file in labelme_files:
        with open(file, "r") as f:
            data = json.load(f)

            # Read image information
            image_filename = os.path.basename(data["imagePath"])
            image_path = os.path.join(os.path.dirname(file), image_filename)
            image = np.array(Image.open(image_path))
            image_height, image_width = image.shape[:2]

            # Create COCO image entry
            coco_image = {
                "file_name": image_filename,
                "height": image_height,
                "width": image_width,
                "id": len(images) + 1  # Start image ID from 1
            }
            images.append(coco_image)

            # Process annotations
            for shape in data["shapes"]:
                label = shape["label"]
                points = shape["points"]

                # Check if category already exists in COCO categories
                if label not in category_mapping:
                    # Create new category
                    category_mapping[label] = category_id
                    category = {
                        "id": category_id,
                        "name": label,
                        "supercategory": label
                    }
                    categories.append(category)
                    category_id += 1

                # Create COCO annotation entry
                annotation = {
                    "id": len(annotations) + 1,  # Start annotation ID from 1
                    "image_id": coco_image["id"],
                    "category_id": category_mapping[label],
                    "segmentation": [np.asarray(points).flatten().tolist()],
                    "bbox": get_bbox(points),
                    "area": get_area(points),
                    "iscrowd": 0
                }
                annotations.append(annotation)

    # Create COCO dataset dictionary
    dataset = {
        "images": images,
        "annotations": annotations,
        "categories": categories
    }

    # Save COCO dataset as JSON
    with open(save_path, "w") as f:
        json.dump(dataset, f)


def get_bbox(points):
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    bbox = [
        np.min(x),  # x_min
        np.min(y),  # y_min
        np.max(x) - np.min(x),  # width
        np.max(y) - np.min(y)   # height
    ]
    return bbox


def get_area(points):
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
    return area

# Example usage
labelme_dir = "Your labelme json file dir"
save_path = "export coco.json dir"
labelme_to_coco(labelme_dir, save_path)
