"""
labelme标注格式转换成png格式，即mask

labelme库中json_to_dataset函数的重写
因为json_to_dataset不考虑全局的类别，
比如当前json中只有4个类别而你的数据集中一共有10个类别
它就会从0开始编号 0, 1, 2, 3
把你的数据集类别编号打乱
所以需要考虑全局类别
"""
import argparse
import base64
import json
import os
import os.path as osp
import PIL.Image
import yaml
from labelme.logger import logger
from labelme import utils

def main():
    #logger.warning('This script is aimed to demonstrate how to convert the'
    #               'JSON file to a single image dataset, and not to handle'
    #               'multiple JSON files to generate a real-use dataset.')

    parser = argparse.ArgumentParser()
    parser.add_argument('json_file')
    parser.add_argument('-o', '--out', default=None)
    # set label names file path
    parser.add_argument('-n','--names',default=None)
    args = parser.parse_args()

    json_file = args.json_file

    if args.out is None:
        out_dir = osp.basename(json_file).replace('.', '_')
        out_dir = osp.join(osp.dirname(json_file), out_dir)
    else:
        out_dir = args.out
    if not osp.exists(out_dir):
        os.mkdir(out_dir)
    
    label_name_to_value = {'_background_': 0}
    
    # add label names to dict    
    if args.names is not None:
        with open(args.names, 'r') as f:
            lines = f.readlines()
        
        count = 0
        for line in lines:
            line = line.strip()
            if line == '':
                continue
                
            label_name_to_value[line] = count
            count += 1
        
    data = json.load(open(json_file))
    imageData = data.get('imageData')

    if not imageData:
        imagePath = os.path.join(os.path.dirname(json_file), data['imagePath'])
        with open(imagePath, 'rb') as f:
            imageData = f.read()
            imageData = base64.b64encode(imageData).decode('utf-8')
    img = utils.img_b64_to_arr(imageData)

    for shape in sorted(data['shapes'], key=lambda x: x['label']):
        label_name = shape['label']
        if label_name in label_name_to_value:
            label_value = label_name_to_value[label_name]
        else:
            label_value = len(label_name_to_value)
            label_name_to_value[label_name] = label_value
    lbl = utils.shapes_to_label(img.shape, data['shapes'], label_name_to_value)

    label_names = [None] * (max(label_name_to_value.values()) +1) # +1是background
    print(len(label_names))
    print(len(label_name_to_value))
    for name, value in label_name_to_value.items():
        print(name, " ", value)
        label_names[value] = name
    lbl_viz = utils.draw_label(lbl, img, label_names)

    PIL.Image.fromarray(img).save(osp.join(out_dir, 'img.png'))
    utils.lblsave(osp.join(out_dir, 'label.png'), lbl)
    PIL.Image.fromarray(lbl_viz).save(osp.join(out_dir, 'label_viz.png'))

    with open(osp.join(out_dir, 'label_names.txt'), 'w') as f:
        print(label_names)
        for lbl_name in label_names:
            f.write(lbl_name + '\n')

    #logger.warning('info.yaml is being replaced by label_names.txt')
    #info = dict(label_names=label_names)
    #with open(osp.join(out_dir, 'info.yaml'), 'w') as f:
    #    yaml.safe_dump(info, f, default_flow_style=False)

    #logger.info('Saved to: {}'.format(out_dir))


if __name__ == '__main__':
    main()
