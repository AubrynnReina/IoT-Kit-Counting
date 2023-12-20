from fastapi import Depends, FastAPI, HTTPException, UploadFile
from sqlalchemy.orm import Session
import uvicorn
import crud
import model
import schema
from db_handler import SessionLocal, engine
from datetime import datetime
from PIL import Image, ImageOps
import io
import torch
import base64
import json
import variables.variables as var
import model_inference as um
import numpy as np
import cv2


model.Base.metadata.create_all(bind=engine)

app = FastAPI()

# model = torch.hub.load(
#     "yolov5", "custom", path="best.pt", source="local", verbose=False
# )

model640, model1563 = um.load_model()


def result_to_json(res: str):
    counts = dict()
    items = json.loads(res)
    for item in items:
        counts[item["name"]] = counts.get(item["name"], 0) + 1
    return counts


@app.get("/")
async def root():
    return {"message": (1, 2)}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/add_student_borrow", response_model=schema.StudentBorrowAdd)
async def add_student_borrow(
    student_id, file: UploadFile, db: Session = Depends(get_db)
):
    content = await file.read()
    img = io.BytesIO()
    img_arr_temp = Image.open(io.BytesIO(content))
    img_arr_temp = ImageOps.exif_transpose(img_arr_temp)
    img_arr_temp.save(img, "JPEG")
    img_arr = cv2.cvtColor(np.array(img_arr_temp), cv2.COLOR_RGB2BGR)
    img_arr = img_arr[..., :3]
    img_res, result_dict = um.inference(model640, model1563, img_arr)
    buffered = io.BytesIO()
    img_res = cv2.cvtColor(img_res, cv2.COLOR_RGB2BGR)
    im_base64 = Image.fromarray(img_res).convert("RGB")
    im_base64.save(buffered, format="JPEG")
    student_existence = crud.get_student_info(db=db, student_id=student_id)
    if not student_existence:
        raise HTTPException(400, "Not a student from FPTU")
    else:
        student_borrow = {
            "student_id": student_id,
            "original_image_borrow": base64.b64encode(img.getvalue()),
            "result_image_borrow": base64.b64encode(buffered.getvalue()),
            "breadboard_borrow": result_dict["Breadboard"],
            "button_borrow": result_dict["Button"],
            "buzzer_borrow": result_dict["Buzzer"],
            "infared_sensor_borrow": result_dict["Infared_Sensor"],
            "keypad_borrow": result_dict["Keypad"],
            "led_matrix_borrow": result_dict["LED_Matrix"],
            "number_led_borrow": result_dict["Number_LED"],
            "photoresistor_borrow": result_dict["Photoresistor"],
            "remote_borrow": result_dict["Remote"],
            "resistor_borrow": result_dict["Resistor"],
            "rheostat_borrow": result_dict["Rheostat"],
            "tool_box_borrow": result_dict["Tool_Box"],
            "tool_box_tray_borrow": result_dict["Tool_Box_Tray"],
            "uno_r3_borrow": result_dict["UNO_R3"],
            "usb_cable_borrow": result_dict["USB_Cable"],
            "ultrasonic_borrow": result_dict["Ultrasonic_Sensor"],
            "wire_borrow": result_dict["Wire"],
            "potentiometer_borrow": result_dict["Potentiometer"],
            "servo_engine_borrow": result_dict["Servo_Engine"],
            "led_borrow": result_dict["LED"],
            "lcd_borrow": result_dict["LCD"],
            "thermistor_borrow": result_dict["Thermistor"],
            "date_time_borrow": datetime.now(),
        }
        return crud.add_student_borrow(
            db=db, student_borrow=schema.StudentBorrowAdd(**student_borrow)
        )


@app.post("/add_student_return", response_model=schema.StudentReturnAdd)
async def add_student_return(
    student_id, file: UploadFile, db: Session = Depends(get_db)
):
    content = await file.read()
    img = io.BytesIO()
    img_arr_temp = Image.open(io.BytesIO(content))
    img_arr_temp = ImageOps.exif_transpose(img_arr_temp)
    img_arr_temp.save(img, "JPEG")
    img_arr = cv2.cvtColor(np.array(img_arr_temp), cv2.COLOR_RGB2BGR)
    img_arr = img_arr[..., :3]
    img_res, result_dict = um.inference(model640, model1563, img_arr)
    buffered = io.BytesIO()
    im_base64 = Image.fromarray(img_res)
    im_base64.save(buffered, format="JPEG")

    student_existence = crud.get_student_borrow_by_id(db=db, student_id=student_id)
    if not student_existence:
        raise HTTPException(400, "Student hasn't borrowed yet")
    else:
        student_return = {
            "student_id": student_id,
            "original_image_return": base64.b64encode(img.getvalue()),
            "result_image_return": base64.b64encode(buffered.getvalue()),
            "breadboard_return": result_dict["Breadboard"],
            "button_return": result_dict["Button"],
            "buzzer_return": result_dict["Buzzer"],
            "infared_sensor_return": result_dict["Infared_Sensor"],
            "keypad_return": result_dict["Keypad"],
            "led_matrix_return": result_dict["LED_Matrix"],
            "number_led_return": result_dict["Number_LED"],
            "photoresistor_return": result_dict["Photoresistor"],
            "remote_return": result_dict["Remote"],
            "resistor_return": result_dict["Resistor"],
            "rheostat_return": result_dict["Rheostat"],
            "tool_box_return": result_dict["Tool_Box"],
            "tool_box_tray_return": result_dict["Tool_Box_Tray"],
            "uno_r3_return": result_dict["UNO_R3"],
            "usb_cable_return": result_dict["USB_Cable"],
            "ultrasonic_return": result_dict["Ultrasonic_Sensor"],
            "wire_return": result_dict["Wire"],
            "potentiometer_return": result_dict["Potentiometer"],
            "servo_engine_return": result_dict["Servo_Engine"],
            "led_return": result_dict["LED"],
            "lcd_return": result_dict["LCD"],
            "thermistor_return": result_dict["Thermistor"],
            "date_time_return": datetime.now(),
        }
        return crud.add_student_return(
            db=db, student_return=schema.StudentReturnAdd(**student_return)
        )


@app.get("/get_student_info")
async def find_student_info(student_id, db: Session = Depends(get_db)):
    result = crud.get_student_info(db=db, student_id=student_id)
    if not result:
        raise HTTPException(400, "Can't find student ID in database")
    else:
        return result


@app.get("/get_student_borrow_by_id")
async def find_student_borrow_info(student_id, db: Session = Depends(get_db)):
    result = crud.get_student_borrow_by_id(db=db, student_id=student_id)
    if result == 0:
        raise HTTPException(400, "Can't find student ID in database")
    else:
        return result


@app.get("/get_student_return_by_id")
async def find_student_return_info(student_id, db: Session = Depends(get_db)):
    result = crud.get_student_return_by_id(db=db, student_id=student_id)
    if result == 0:
        raise HTTPException(400, "Can't find student ID in database")
    else:
        return result


@app.put("/update_student_borrow_by_id")
async def update_student_borrow_info(
    student_id, update_param: schema.StudentBorrowUpdate, db: Session = Depends(get_db)
):
    student_existence = crud.get_student_borrow_by_id(db=db, student_id=student_id)
    if not student_existence:
        raise HTTPException(400, "Can't find student ID in database")
    else:
        return crud.update_student_borrow(
            db=db, student_id=student_id, details=update_param
        )


@app.put("/update_student_return_by_id")
async def update_student_return_info(
    student_id, update_param: schema.StudentReturnUpdate, db: Session = Depends(get_db)
):
    student_existence = crud.get_student_return_by_id(db=db, student_id=student_id)
    if not student_existence:
        raise HTTPException(400, "Can't find student ID in database")
    else:
        return crud.update_student_return(
            db=db, student_id=student_id, details=update_param
        )


if __name__ == "__main__":
    uvicorn.run("application:app", host="127.0.0.1", port=8080, reload=True)
