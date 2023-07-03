"""
labelme2png.py 生成的标注文件和图片在一个目录中
这个脚本将划分成img和labels两个目录，且图片和标注文件同名
"""
import os
import shutil

input_dir = 'labelme2png生成的目录'
output_img_dir = 'img'
output_labels_dir = 'labels'

# 创建输出文件夹
os.makedirs(output_img_dir, exist_ok=True)
os.makedirs(output_labels_dir, exist_ok=True)

# 遍历标注文件夹
for folder_name in os.listdir(input_dir):
    folder_path = os.path.join(input_dir, folder_name)
    if os.path.isdir(folder_path):
        # 获取数字文件夹中的img.png和label.png文件路径
        img_path = os.path.join(folder_path, 'img.png')
        label_path = os.path.join(folder_path, 'label.png')
        
        # 设置输出路径和文件名
        output_img_path = os.path.join(output_img_dir, folder_name + '.png')
        output_label_path = os.path.join(output_labels_dir, folder_name + '.png')
        
        # 将img.png和label.png文件复制到输出文件夹并重命名
        shutil.copy(img_path, output_img_path)
        shutil.copy(label_path, output_label_path)
