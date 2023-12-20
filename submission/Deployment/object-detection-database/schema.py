from pydantic import BaseModel
from datetime import datetime


class StudentBase(BaseModel):
    student_id: str


class StudentBorrowAdd(StudentBase):
    original_image_borrow: bytes
    result_image_borrow: bytes
    breadboard_borrow: int
    button_borrow: int
    buzzer_borrow: int
    infared_sensor_borrow: int
    keypad_borrow: int
    led_matrix_borrow: int
    number_led_borrow: int
    photoresistor_borrow: int
    remote_borrow: int
    resistor_borrow: int
    rheostat_borrow: int
    tool_box_borrow: int
    tool_box_tray_borrow: int
    uno_r3_borrow: int
    usb_cable_borrow: int
    ultrasonic_borrow: int
    wire_borrow: int
    potentiometer_borrow: int
    servo_engine_borrow: int
    led_borrow: int
    lcd_borrow: int
    thermistor_borrow: int
    date_time_borrow: datetime

    class Config:
        orm_mode = True


class StudentReturnAdd(StudentBase):
    original_image_return: bytes
    result_image_return: bytes
    breadboard_return: int
    button_return: int
    buzzer_return: int
    infared_sensor_return: int
    keypad_return: int
    led_matrix_return: int
    number_led_return: int
    photoresistor_return: int
    remote_return: int
    resistor_return: int
    rheostat_return: int
    tool_box_return: int
    tool_box_tray_return: int
    uno_r3_return: int
    usb_cable_return: int
    ultrasonic_return: int
    wire_return: int
    potentiometer_return: int
    servo_engine_return: int
    led_return: int
    lcd_return: int
    thermistor_return: int
    date_time_return: datetime

    class Config:
        orm_mode = True


class StudentBorrowUpdate(BaseModel):
    breadboard_borrow: int
    button_borrow: int
    buzzer_borrow: int
    infared_sensor_borrow: int
    keypad_borrow: int
    led_matrix_borrow: int
    number_led_borrow: int
    photoresistor_borrow: int
    remote_borrow: int
    resistor_borrow: int
    rheostat_borrow: int
    tool_box_borrow: int
    tool_box_tray_borrow: int
    uno_r3_borrow: int
    usb_cable_borrow: int
    ultrasonic_borrow: int
    wire_borrow: int
    potentiometer_borrow: int
    servo_engine_borrow: int
    led_borrow: int
    lcd_borrow: int
    thermistor_borrow: int

    class Config:
        orm_mode = True


class StudentReturnUpdate(BaseModel):
    breadboard_return: int
    button_return: int
    buzzer_return: int
    infared_sensor_return: int
    keypad_return: int
    led_matrix_return: int
    number_led_return: int
    photoresistor_return: int
    remote_return: int
    resistor_return: int
    rheostat_return: int
    tool_box_return: int
    tool_box_tray_return: int
    uno_r3_return: int
    usb_cable_return: int
    ultrasonic_return: int
    wire_return: int
    potentiometer_return: int
    servo_engine_return: int
    led_return: int
    lcd_return: int
    thermistor_return: int

    class Config:
        orm_mode = True
