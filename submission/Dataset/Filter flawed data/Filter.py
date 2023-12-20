import glob
import os
from pathlib import Path
import shutil

DATASET_PATH = 'Furniture-Detection-2'
FULL_DATASET_PATH = Path(Path.cwd(), DATASET_PATH)

task_types = ['train', 'valid', 'test']
for task_type in task_types:
    print(task_type)
    os.mkdir(Path(FULL_DATASET_PATH, task_type + '_new'))
    os.mkdir(Path(FULL_DATASET_PATH, task_type + '_new', 'labels'))
    os.mkdir(Path(FULL_DATASET_PATH, task_type + '_new', 'images'))

    label_path = Path(FULL_DATASET_PATH, task_type, 'labels')

    new_label_path = Path(FULL_DATASET_PATH, task_type + '_new', 'labels')
    new_image_path = Path(FULL_DATASET_PATH, task_type + '_new', 'images')

    for file in glob.glob(str(Path(label_path, '*'))):
        readable_file = open(file, mode='rt+')
        data = readable_file.readlines()

        for label in data:
            class_num = label.split()[0]
            if int(class_num) in [2, 5]:  # 2 is Door, 5 is Stairs
                img_file = file.replace('labels', 'images')
                img_file = img_file.replace(file[-3:], 'jpg')
                shutil.copy(file, new_label_path)
                shutil.copy(img_file, new_image_path)
                break
