from sqlalchemy.orm import Session
import model
import schema
from sqlalchemy import select


def add_student_borrow(db: Session, student_borrow: schema.StudentBorrowAdd):
    borrow_details = model.StudentBorrow(
        student_id=student_borrow.student_id,
        original_image_borrow=student_borrow.original_image_borrow,
        result_image_borrow=student_borrow.result_image_borrow,
        breadboard_borrow=student_borrow.breadboard_borrow,
        button_borrow=student_borrow.button_borrow,
        buzzer_borrow=student_borrow.buzzer_borrow,
        infared_sensor_borrow=student_borrow.infared_sensor_borrow,
        keypad_borrow=student_borrow.keypad_borrow,
        led_matrix_borrow=student_borrow.led_matrix_borrow,
        number_led_borrow=student_borrow.number_led_borrow,
        photoresistor_borrow=student_borrow.photoresistor_borrow,
        remote_borrow=student_borrow.remote_borrow,
        resistor_borrow=student_borrow.resistor_borrow,
        rheostat_borrow=student_borrow.rheostat_borrow,
        tool_box_borrow=student_borrow.tool_box_borrow,
        tool_box_tray_borrow=student_borrow.tool_box_tray_borrow,
        uno_r3_borrow=student_borrow.uno_r3_borrow,
        usb_cable_borrow=student_borrow.usb_cable_borrow,
        ultrasonic_borrow=student_borrow.ultrasonic_borrow,
        wire_borrow=student_borrow.wire_borrow,
        potentiometer_borrow=student_borrow.potentiometer_borrow,
        servo_engine_borrow=student_borrow.servo_engine_borrow,
        led_borrow=student_borrow.led_borrow,
        lcd_borrow=student_borrow.lcd_borrow,
        thermistor_borrow=student_borrow.thermistor_borrow,
        date_time_borrow=student_borrow.date_time_borrow,
    )
    db.add(borrow_details)
    db.commit()
    db.refresh(borrow_details)
    return model.StudentBorrow(**student_borrow.dict())


def add_student_return(db: Session, student_return: schema.StudentReturnAdd):
    return_details = model.StudentReturn(
        student_id=student_return.student_id,
        original_image_return=student_return.original_image_return,
        result_image_return=student_return.result_image_return,
        breadboard_return=student_return.breadboard_return,
        button_return=student_return.button_return,
        buzzer_return=student_return.buzzer_return,
        infared_sensor_return=student_return.infared_sensor_return,
        keypad_return=student_return.keypad_return,
        led_matrix_return=student_return.led_matrix_return,
        number_led_return=student_return.number_led_return,
        photoresistor_return=student_return.photoresistor_return,
        remote_return=student_return.remote_return,
        resistor_return=student_return.resistor_return,
        rheostat_return=student_return.rheostat_return,
        tool_box_return=student_return.tool_box_return,
        tool_box_tray_return=student_return.tool_box_tray_return,
        uno_r3_return=student_return.uno_r3_return,
        usb_cable_return=student_return.usb_cable_return,
        ultrasonic_return=student_return.ultrasonic_return,
        wire_return=student_return.wire_return,
        potentiometer_return=student_return.potentiometer_return,
        servo_engine_return=student_return.servo_engine_return,
        led_return=student_return.led_return,
        lcd_return=student_return.lcd_return,
        thermistor_return=student_return.thermistor_return,
        date_time_return=student_return.date_time_return,
    )
    db.add(return_details)
    db.commit()
    db.refresh(return_details)
    return model.StudentReturn(**student_return.dict())


def get_student_info(db: Session, student_id: str):
    return (
        db.query(model.StudentInfo)
        .filter(model.StudentInfo.student_id == student_id)
        .first()
    )


def get_student_borrow_by_id(db: Session, student_id: str):
    result = db.execute(
        select(
            model.StudentInfo.student_id,
            model.StudentInfo.student_name,
            model.StudentInfo.student_class,
            model.StudentBorrow.original_image_borrow,
            model.StudentBorrow.result_image_borrow,
            model.StudentBorrow.breadboard_borrow,
            model.StudentBorrow.button_borrow,
            model.StudentBorrow.buzzer_borrow,
            model.StudentBorrow.infared_sensor_borrow,
            model.StudentBorrow.keypad_borrow,
            model.StudentBorrow.led_matrix_borrow,
            model.StudentBorrow.number_led_borrow,
            model.StudentBorrow.photoresistor_borrow,
            model.StudentBorrow.remote_borrow,
            model.StudentBorrow.resistor_borrow,
            model.StudentBorrow.rheostat_borrow,
            model.StudentBorrow.tool_box_borrow,
            model.StudentBorrow.tool_box_tray_borrow,
            model.StudentBorrow.uno_r3_borrow,
            model.StudentBorrow.usb_cable_borrow,
            model.StudentBorrow.ultrasonic_borrow,
            model.StudentBorrow.wire_borrow,
            model.StudentBorrow.potentiometer_borrow,
            model.StudentBorrow.servo_engine_borrow,
            model.StudentBorrow.led_borrow,
            model.StudentBorrow.lcd_borrow,
            model.StudentBorrow.thermistor_borrow,
            model.StudentBorrow.date_time_borrow,
        )
        .join(
            model.StudentBorrow,
            model.StudentInfo.student_id == model.StudentBorrow.student_id,
        )
        .order_by(model.StudentBorrow.date_time_borrow.desc())
        .where(model.StudentInfo.student_id == student_id)
    ).first()

    try:
        return {
            "Student ID": result.student_id,
            "Student Name": result.student_name,
            "Student Class": result.student_class,
            "Original Image": result.original_image_borrow,
            "Result Image": result.result_image_borrow,
            "Breadboard": result.breadboard_borrow,
            "Button": result.button_borrow,
            "Buzzer": result.buzzer_borrow,
            "Infared sensor": result.infared_sensor_borrow,
            "Keypad": result.keypad_borrow,
            "Led matrix": result.led_matrix_borrow,
            "Number led": result.number_led_borrow,
            "Photoresistor": result.photoresistor_borrow,
            "Remote": result.remote_borrow,
            "Resistor": result.resistor_borrow,
            "Rheostat": result.rheostat_borrow,
            "Tool box": result.tool_box_borrow,
            "Tool box tray": result.tool_box_tray_borrow,
            "Uno R3": result.uno_r3_borrow,
            "USB Cable": result.usb_cable_borrow,
            "Ultrasonic": result.ultrasonic_borrow,
            "Wire": result.wire_borrow,
            "Potentiometer": result.potentiometer_borrow,
            "Servo engine": result.servo_engine_borrow,
            "Led": result.led_borrow,
            "LCD": result.lcd_borrow,
            "Thermistor": result.thermistor_borrow,
            "Time borrow": result.date_time_borrow,
        }
    except:
        return 0


"""
select student_info.student_id, student_info.student_name, student_info.student_class,student_borrow.breadboard_borrow
from student_info
join student_borrow on student_info.student_id == student_borrow.student_id
"""


def get_student_return_by_id(db: Session, student_id: str):
    result = db.execute(
        select(
            model.StudentInfo.student_id,
            model.StudentInfo.student_name,
            model.StudentInfo.student_class,
            model.StudentReturn.original_image_return,
            model.StudentReturn.result_image_return,
            model.StudentReturn.breadboard_return,
            model.StudentReturn.button_return,
            model.StudentReturn.buzzer_return,
            model.StudentReturn.infared_sensor_return,
            model.StudentReturn.keypad_return,
            model.StudentReturn.led_matrix_return,
            model.StudentReturn.number_led_return,
            model.StudentReturn.photoresistor_return,
            model.StudentReturn.remote_return,
            model.StudentReturn.resistor_return,
            model.StudentReturn.rheostat_return,
            model.StudentReturn.tool_box_return,
            model.StudentReturn.tool_box_tray_return,
            model.StudentReturn.uno_r3_return,
            model.StudentReturn.usb_cable_return,
            model.StudentReturn.ultrasonic_return,
            model.StudentReturn.wire_return,
            model.StudentReturn.potentiometer_return,
            model.StudentReturn.servo_engine_return,
            model.StudentReturn.led_return,
            model.StudentReturn.lcd_return,
            model.StudentReturn.thermistor_return,
            model.StudentReturn.date_time_return,
        )
        .join(
            model.StudentBorrow,
            model.StudentInfo.student_id == model.StudentBorrow.student_id,
        )
        .order_by(model.StudentReturn.date_time_return.desc())
        .where(model.StudentInfo.student_id == student_id)
    ).first()

    try:
        return {
            "Student ID": result.student_id,
            "Student Name": result.student_name,
            "Student Class": result.student_class,
            "Original Image": result.original_image_return,
            "Result Image": result.result_image_return,
            "Breadboard": result.breadboard_return,
            "Button": result.button_return,
            "Buzzer": result.buzzer_return,
            "Infared sensor": result.infared_sensor_return,
            "Keypad": result.keypad_return,
            "Led matrix": result.led_matrix_return,
            "Number led": result.number_led_return,
            "Photoresistor": result.photoresistor_return,
            "Remote": result.remote_return,
            "Resistor": result.resistor_return,
            "Rheostat": result.rheostat_return,
            "Tool box": result.tool_box_return,
            "Tool box tray": result.tool_box_tray_return,
            "Uno R3": result.uno_r3_return,
            "USB Cable": result.usb_cable_return,
            "Ultrasonic": result.ultrasonic_return,
            "Wire": result.wire_return,
            "Potentiometer": result.potentiometer_return,
            "Servo engine": result.servo_engine_return,
            "Led": result.led_return,
            "LCD": result.lcd_return,
            "Thermistor": result.thermistor_return,
            "Time return": result.date_time_return,
        }
    except:
        return 0


def update_student_borrow(
    db: Session, student_id: str, details: schema.StudentBorrowUpdate
):
    db.query(model.StudentBorrow).filter(
        model.StudentBorrow.student_id == student_id
    ).update(vars(details))
    db.commit()
    return (
        db.query(model.StudentBorrow)
        .filter(model.StudentBorrow.student_id == student_id)
        .first()
    )


def update_student_return(
    db: Session, student_id: str, details: schema.StudentReturnUpdate
):
    db.query(model.StudentReturn).filter(
        model.StudentReturn.student_id == student_id
    ).update(vars(details))
    db.commit()
    return (
        db.query(model.StudentReturn)
        .filter(model.StudentReturn.student_id == student_id)
        .first()
    )
