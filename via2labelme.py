"""
VGG Image Annotator format to Labelme
via标注格式转换成labelme标注格式 (poly)
"""
import os
import json
import base64
from PIL import Image

def convert_via_to_labelme(via_json_file, output_dir):
    with open(via_json_file, 'r') as f:
        via_data = json.load(f)

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Convert VIA annotations to LabelMe format
    for img_data in via_data.values():
        regions = img_data['regions']
        image_filename = img_data['filename']
        # image_width = img_data['size'][0]
        # image_height = img_data['size'][1]

        # Read original image and encode it as base64
        image_path = os.path.join(os.path.dirname(via_json_file), image_filename)
        image_pre = image_filename.split('.')[0]
        # if image_pre in image_list:
        #     print("Changing...")
        #     im = Image.open(image_path)
        #     im = im.rotate(180)
        #     im.save(image_path)
        # 如果你转换的图片经过旋转，请自行加图片名字添加到image_list中，并取消上行的注释

        with open(image_path, 'rb') as img_file:
            image_data = img_file.read()
            image_data_base64 = base64.b64encode(image_data).decode('utf-8')

        # Create LabelMe data for the image
        labelme_data = {
            'version': '5.1.1',
            'flags': {},
            'shapes': [],
            'imagePath': image_filename,
            'imageData': image_data_base64,
            # 'imageWidth': image_width,
            # 'imageHeight': image_height
        }

        for region in regions:
            all_points_x = [float(x) for x in region['shape_attributes']['all_points_x']]
            all_points_y = [float(y) for y in region['shape_attributes']['all_points_y']]
            
            shape = {
                'label': region['region_attributes']['tooth'],
                'points': list(zip(all_points_x, all_points_y)),
                'group_id': None,
                'shape_type': 'polygon',
                'flags': {}
            }
            labelme_data['shapes'].append(shape)

        # Save the LabelMe annotations to a JSON file
        output_json_file = os.path.join(output_dir, os.path.splitext(image_filename)[0] + '.json')
        with open(output_json_file, 'w') as f:
            json.dump(labelme_data, f, indent=4)

        print('Conversion complete for', image_filename)


# Usage example
via_json_file = 'Your json file dir'
output_dir = 'Your output dir'
convert_via_to_labelme(via_json_file, output_dir)
