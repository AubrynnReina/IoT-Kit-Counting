import glob

from pathlib import Path

DATASET_PATH = 'Furniture-Detection-2'
FULL_DATASET_PATH = Path(Path.cwd(), DATASET_PATH)

label_path = Path(FULL_DATASET_PATH, 'train_new', 'labels')

for file in glob.glob(str(Path(label_path, '*'))):
    readable_file = open(file, mode='rt+')
    data = readable_file.readlines()
    print(data)