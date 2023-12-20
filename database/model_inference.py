from ultralytics.utils.plotting import Annotator, colors
import numpy as np
import torch, torchvision
import variables.variables as var


def xyn2xy(x, w=640, h=640, padw=0, padh=0):
    # Convert normalized segments into pixel segments, shape (n,2)
    y = x.clone() if isinstance(x, torch.Tensor) else np.copy(x)
    y[..., 0] = w * x[..., 0] + padw  # top left x
    y[..., 1] = h * x[..., 1] + padh  # top left y
    return y


def list_to_json(items: list):
    counts = dict()
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts


def make_image_wbbox(image, preds, hide_conf=False, hide_labels=False):
    print("\nCombining Image and Labels...")
    im0 = np.array(image)
    imgsz = im0.shape[:2] # h w
    h, w = imgsz

    line_thickness = 1 * int(imgsz[0] / 640)

    # Process predictions, plot onto image
    for i, bbox in enumerate(preds):
        xyxyn, conf, c = bbox[:4], float(bbox[4]), int(float(bbox[5]))
        # print('xyxyn,  conf, classi', xyxyn, conf, c )
        xyxy_list = [
            xyn2xy(xyxyn[:2], w=imgsz[1], h=imgsz[0]),
            xyn2xy(xyxyn[2:], w=imgsz[1], h=imgsz[0]),
        ]

        xyxy = torch.cat((xyxy_list[0], xyxy_list[1]), 0)
        annotator = Annotator(im0, line_width=line_thickness, example=str(var.names))
        label = (
            None
            if hide_labels
            else (var.names[c] if hide_conf else f"{var.names[c]} {conf:.2f}")
        )
        # print(' xyxy,  conf, classi', xyxy, conf, c )
        annotator.box_label(xyxy, label, color=colors(c, True))
    img_with_bboxes = annotator.result()
    return img_with_bboxes


def load_model():
    model640 = torch.hub.load(
        "yolov5",
        "custom",
        path="best.pt",
        source="local",
        verbose=False,
    )
    model640.classes = var.resize_mapping["640"]
    model640.hide_conf = True
    model640.agnostic = True
    model640.conf = 0.45

    model1536 = torch.hub.load(
        "yolov5",
        "custom",
        path="best.pt",
        source="local",
        verbose=False,
    )
    model1536.classes = var.resize_mapping["1536"]
    model1536.hide_conf = True
    model1536.agnostic = True

    return model640, model1536


def inference(model640, model1536, img):
    img2 = img.copy()
    with torch.no_grad():
        results = model640(img, size=640)  # inference
        results1536 = model1536(img, size=1536)  # inference

    xyxyn1 = results.xyxyn[0]
    xyxyn2 = results1536.xyxyn[0]
    xyxyn12 = torch.cat((xyxyn1, xyxyn2), 0)
    xyxyn12_nms_id = torchvision.ops.nms(
        boxes=xyxyn12[:, :4], scores=xyxyn12[:, -2], iou_threshold=0.45
    )
    xyxyn12_nms_ed = torch.index_select(xyxyn12, dim=0, index=xyxyn12_nms_id)
    img_wbbox = make_image_wbbox(img2, xyxyn12_nms_ed)
    results_dict = {
        **var.temp_result,
        **list_to_json([var.names[int(i)] for i in xyxyn12_nms_ed[:, -1].tolist()]),
    }
    return img_wbbox, results_dict
