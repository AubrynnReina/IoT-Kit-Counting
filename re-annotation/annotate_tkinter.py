import tkinter as tk
from PIL import ImageTk, Image
import os
import cv2
import json
global DS_SPLIT
global current_id       # keep track of bbox_id in each image
global next_id          # keep track of bbox_id in each image
global image_file
global label_file

DS_PATH = os.path.join("C:\FPTU_Capstone\Filtered flawed data\Filtered flawed data\Furniture-Detection-2")
DS_SPLIT = "valid"

'''
    HOW TO RUN
    - Change the `DS_PATH`, `DS_SPLIT`, and `ANNOTATING_FILE`
    - Run
'''

DS_PATH = os.path.join("data_Furniture-Detection-2")
DS_SPLIT = "train"
ANNOTATING_FILE = 'file_name.json'  # json file of image-names

# -----------------------------------------------------------------------------

def process_img(image_file:str, label_file:str, _current_id=0, max_img_size=(800, 300)) -> (Image, int, int):
    '''Read image - Draw bbox - Return image'''

    print(f"---\nImage: {image_file}")
    print('Label_file: ', label_file)
    print('Annotating bbox_id: ', _current_id)

    # Get object(bbox) info from label file
    with open(label_file, 'r') as f:
        label_content = f.read()
    label_content_split = label_content.split()
    number_of_objects = int(len(label_content_split)/5)
    if _current_id+1 == number_of_objects: # this is the last bbox, next iter will be another image
        _next_id = 0  
    else:
        _next_id = _current_id +1          # this image is not done yet

    object_list = [label_content_split[i:i+5] for i in range(0, len(label_content_split), 5)] # [[class, x, y, w, h],
                                                                                              #   [class, x, y, w, h], ...]
    cur_object = object_list[_current_id]
    object_class_id = int(cur_object[0])    # object: [class, x, y, w, h]
    object_class_mapping = {2: 'Door', 5: 'Stairs'}     # from file `data.yaml``
    object_class_name = object_class_mapping.get(object_class_id, "others")
    print('Current object info: ', cur_object)

    # Read image
    img =cv2.imread(image_file)
    w,h = img.shape[:2] 
    center_x_ratio, center_y_ratio, w_ratio, h_ratio = [float(i) for i in cur_object[1:]]
    x1, x2 = [int(w*x_i) for x_i in (center_x_ratio-w_ratio/2, center_x_ratio+w_ratio/2)]
    y1, y2 = [int(h*y_i) for y_i in (center_y_ratio-h_ratio/2, center_y_ratio+h_ratio/2)]

    # Add bounding box & labelled_class to image
    img = cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
    img = cv2.putText(img, f"{object_class_name}",(x1, y1+50),
                      cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5,
                      color=(0, 0, 200), thickness=5)
    
    # convert cv2 to PIL image type
    tmp_color_coverted = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(tmp_color_coverted)

    # resize PIL image
    w, h = pil_image.size
    ratio = min(max_img_size[0]/w, max_img_size[1]/h)
    newsize = (int(w*ratio), int(h*ratio))
    resized_image = pil_image.resize(newsize, Image.LANCZOS)
    return resized_image, _current_id, _next_id # next_id=0: start new image next iter; 1, 2, ..: starting_id of the same image on next iterate

def makestr_status(image_name, bbox_id) -> str:
    return f'Image: {image_name}, bbox_id: {bbox_id}'

def next_button(): # command for the `Next` button
    '''Save annotation result to file, then load new image to continue annotating'''
    
    global image_file
    global label_file
    global next_id
    global current_id
    global DS_SPLIT
    new_class_id_mapping = {2:5, 5:2}

    # --- [ save previous annotation ] ---
    with open(label_file, 'r') as f:
        origin_label_splitted = f.read().split()

    # Get object(bbox) info from (original)label file
    object_list = [origin_label_splitted[i:i+5] for i in range(0, len(origin_label_splitted), 5)] # [[class, x, y, w, h],
                                                                                #   [class, x, y, w, h], ...]
    cur_object = object_list[current_id]
    # print('Current object info: ', cur_object)

    # Change the class_id if answer=='F', else, answer=='T', we will save the same thing to label_new
    origin_class_id = int(cur_object[0])
    answer = entry_noidung.get().strip()
    image_name = os.path.basename(image_file)

    if answer not in ('T', 'F'):
        print('Only T/F is expected.')
        label_status.config(text='Only T/F is expected.')
        return None
    elif answer == 'F':
        new_class_id = new_class_id_mapping.get(origin_class_id, origin_class_id) # case: class=3 -> keep it as 3
        new_label_content = cur_object.copy()
        new_label_content[0] = new_class_id
        status_str = f'Status: CLASS CHANGED for image {image_name}.'
    else: # answer =='T'
        new_label_content = cur_object
        status_str = f'Status: CLASS KEPT AS ORIGIN for image {image_name}.'
    label_name = os.path.basename(label_file)
    label_file_output = os.path.join(DS_PATH, DS_SPLIT, "labels_new", label_name)

    print('After-anno object info: ' , new_label_content)

    # Write to label_new file
    content_to_write = " ".join(str(i) for i in new_label_content)
    if os.path.exists(label_file_output):
        # print('appending to existed label file.')
        content_to_write = '\n' + content_to_write

    with open(label_file_output, 'a') as f:
        f.write(content_to_write)
    print('New label(s) saved to file: ', label_file_output)
    
    label_status.config(text=status_str)


    # --- [ load next image bounding box ] ----
    if next_id==0: # get next image from the remanining list
        try:
            image_name = next(img_list_generator)
        except StopIteration:
            print('All images have been annotated! This work is done.')
            label_status.config(text='Status: All images for this split have been annotated! Change the split and re-run.',
                                fg= "red", font=("Helvetica", 25))

    
        label_name = image_name[:-4] + ".txt"
        image_file = os.path.join(DS_PATH, DS_SPLIT, "images", image_name)
        label_file = os.path.join(DS_PATH, DS_SPLIT, "labels", label_name)


    start_id = next_id
    img, current_id, next_id = process_img(image_file, label_file, start_id)

    imgTK = ImageTk.PhotoImage(img)
    label_img.config(image=imgTK)
    label_img.image = imgTK
    entry_noidung.delete(0, tk.END)
    default_answer = 'T'
    entry_noidung.insert(0, default_answer)
    label_imgname.config(text=makestr_status(image_file, current_id))

def resume_annotating(subset, all_images_file) -> list:
    '''Scan the folders, return a list of remaining images to annotate'''

    if all_images_file == 'all':
        all_images_file = 'all_images.json'
        # create file that list all images (if not exist)
        if not os.path.exists(all_images_file):
            all_images = {}
            for subset in ["train", "valid", "test"]:
                split_images = os.listdir(os.path.join(DS_PATH, subset, "labels"))
                # print(split_images)
                all_images[subset] = [image[:-4]+'.jpg' for image in split_images]
            # print(all_images)
            with open(all_images_file, 'w') as f:
                json.dump(all_images, f)

    # get all_images list
    with open(all_images_file, 'r') as f:
        all_images = json.load(f)
        all_images_split = all_images[DS_SPLIT]
    print(f'Number of images in [{DS_SPLIT}] split: ', len(all_images_split))

    # list labelled images
    labelled_images = []
    split_images = os.listdir(os.path.join(DS_PATH, subset, os.path.basename(newlabel_folder)))
    labelled_images += [image[:-4]+'.jpg' for image in split_images]

    # get remaining_images list
    remaning_images = [image for image in all_images_split if image not in labelled_images]
    print('remaining images:', len(remaning_images))
    return remaning_images

# -----------------------------------------------------------------------------

for subset in ["train", "valid", "test"]:
    newlabel_folder = os.path.join(DS_PATH, subset, "labels_new")
    if not os.path.exists(newlabel_folder):
        os.mkdir(newlabel_folder)

img_list = resume_annotating(DS_SPLIT, ANNOTATING_FILE)
img_list_generator = iter(img_list)
try:
    first_image_name = next(img_list_generator)
except:
    first_image_name = None
    print('List empty, No more image to annotate')
    exit()
first_label_name = first_image_name[:-4] + ".txt"
image_file = os.path.join(DS_PATH, DS_SPLIT, "images", first_image_name) # first
label_file = os.path.join(DS_PATH, DS_SPLIT, "labels", first_label_name) # first
first_image, current_id, next_id = process_img(image_file, label_file)

# ------------------------------------------------------------------------------

window = tk.Tk()
window.title('Re-annotation - Furniture - Capstone2023')
window.geometry("1500x600")  
blankframe = tk.Frame(window, width=600, height=20)
blankframe.pack()


title_frame = tk.Frame(window, width=600, height=600)
title_frame.pack()

label_title = tk.Label(title_frame, text='Door/Stair Annotating', font=("Helvetica 30 bold"))
label_title.pack(pady=(0, 50))

imgTK = ImageTk.PhotoImage(first_image)
label_img =  tk.Label(title_frame, image=imgTK, height=300)
label_img.pack()

label_imgname = tk.Label(title_frame, text=makestr_status(image_file, current_id))
label_imgname.pack()

label_instruction = tk.Label(title_frame, text='Enter T/F. Default=T', font='bold')
label_instruction.pack(pady=(20, 0))

entry_noidung = tk.Entry(title_frame, width=60,font=('Georgia 12'))
predicted_text = "T"
entry_noidung.insert(0, predicted_text)
entry_noidung.pack()

label_status = tk.Label(title_frame, text='Status: _')
label_status.pack(side='left')

frame_next_button = tk.Frame(window, width=600, height=200)
frame_next_button.pack()


button_next_item = tk.Button(frame_next_button, text='Next', command=next_button)
button_next_item.pack(side='bottom', pady=(50, 0))

window.bind('<Return>', lambda event:next_button())

window.mainloop()