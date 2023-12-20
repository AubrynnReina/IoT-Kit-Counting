from ultralytics.utils.plotting import Annotator, colors
# names should be imported from data.yaml file
names = ['Breadboard', 'Button', 'Buzzer', 'Infared_Sensor', 'Keypad', 'LCD', 'LED', 'LED_Matrix', 'Number_LED', 'Photoresistor', 'Potentiometer', 'Remote', 'Resistor', 'Rheostat', 'Servo_Engine', 'Thermistor', 'Tool_Box', 'Tool_Box_Tray', 'UNO_R3', 'USB_Cable', 'Ultrasonic_Sensor', 'Wire']
from utils.general import xywhn2xyxy, xyn2xy # yolov5.utils


def make_image_wbbox(image, preds, hide_conf=False, hide_labels=False):
  print('\nCombining Image and Labels...')
  im0 = image
  imgsz = im0.shape[:2] # h w
  h, w = imgsz
  print('Shape of the output image is [w, h]: ', imgsz[1], imgsz[0])

  line_thickness = 1* int(imgsz[0]/640)

  # Process predictions, plot onto image
  for i, bbox in enumerate(preds):
      xyxyn, conf, c = bbox[:4], float(bbox[4]), int(float(bbox[5]))
      # print('xyxyn,  conf, classi', xyxyn, conf, c )
      xyxy_list=[xyn2xy(xyxyn[:2], w=imgsz[1], h=imgsz[0]), xyn2xy(xyxyn[2:], w=imgsz[1], h=imgsz[0])]

      xyxy = torch.cat((xyxy_list[0], xyxy_list[1]), 0)
      annotator = Annotator(im0, line_width=line_thickness, example=str(names))
      label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
      # print(' xyxy,  conf, classi', xyxy, conf, c )
      annotator.box_label(xyxy, label, color=colors(c, True))
  img_with_bboxes = annotator.result()
  return img_with_bboxes

# #############################################################
import torch, torchvision
import cv2
resize_mapping = {"640": [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 13, 16, 17, 18, 19, 20, 21], "1536": [6, 12, 14, 15]} 

yolov5path = "/content/drive/MyDrive/AI_Engineer/yolov5_train/iot/object-detection_Nov25/yolov5"
bestpt = '/content/drive/MyDrive/AI_Engineer/yolov5_train/iot/v5x6_fullCable_n_Synthetic2/weights/best.pt'

conf = 0.3  # NMS confidence threshold
iou = 0.45  # NMS IoU threshold
hide_conf = True
agnostic = True


model640 = torch.hub.load(
    yolov5path, "custom", path=bestpt, source="local", verbose=False,
)
model640.classes = resize_mapping["640"]
model640.hide_conf = hide_conf
model640.agnostic = agnostic
model640.conf = conf
model640.iou = iou

model1536 = torch.hub.load(
    yolov5path, "custom", path=bestpt, source="local", verbose=False,
)
model1536.classes = resize_mapping["1536"]
model1536.hide_conf = hide_conf
model1536.agnostic = agnostic
model1536.conf = conf
model1536.iou = iou


ima = cv2.imread('/content/drive/MyDrive/AI_Engineer/Dataset-IoT/Nov27-testmoremore/good_1701152549038.jpg')
ima2 =ima.copy()

with torch.no_grad():
    results = model640(ima, size=640)         # inference
    results1536 = model1536(ima, size=1536)   # inference

xyxyn1 = results.xyxyn[0]
xyxyn2 = results1536.xyxyn[0]
# print(f"xyxyn1 is : {xyxyn1}")
# print(f"xyxyn2 is: {xyxyn2}")

# Concat 2 results, then perform nms
xyxyn12 = torch.cat((xyxyn1, xyxyn2), 0)

xyxyn12_nms_id = torchvision.ops.nms(boxes=xyxyn12[:,:4], scores=xyxyn12[:,-1], iou_threshold=0.45)
xyxyn12_nms_ed = torch.index_select(xyxyn12, dim=0, index=xyxyn12_nms_id)

img_wbbox = make_image_wbbox(ima2, xyxyn12_nms_ed)


savepath = '/content/result_torchhub2.jpg'
cv2.imwrite(savepath, img_wbbox)
print(f'img saved to {savepath}')
