import webbrowser
import glob
from pathlib import Path
from PIL import Image

DATASET_PATH = 'Furniture-Detection-2'
FULL_DATASET_PATH = Path(Path.cwd(), DATASET_PATH)

label_path = Path(FULL_DATASET_PATH, 'train', 'labels')

for file in glob.glob(str(Path(label_path, '*'))):
    webbrowser.open(file)
    img_file = file.replace('labels', 'images')
    img_file = img_file.replace(file[-3:], 'jpg')
    img = Image.open(img_file)
    img.show()
    input('Press Enter to continue...')
