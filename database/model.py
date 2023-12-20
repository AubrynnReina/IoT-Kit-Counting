from sqlalchemy import Boolean, Column, Integer, String, LargeBinary, DateTime
from db_handler import Base


class StudentInfo(Base):
    __tablename__ = "student_info"
    student_id = Column(String, primary_key=True, nullable=False)
    student_name = Column(String, index=True, nullable=False)
    student_class = Column(String(255), index=True, nullable=False)


class StudentBorrow(Base):
    __tablename__ = "student_borrow"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    student_id = Column(String, nullable=False)
    original_image_borrow = Column(LargeBinary, nullable=False)
    result_image_borrow = Column(LargeBinary, nullable=False)
    breadboard_borrow = Column(Integer, nullable=False)
    button_borrow = Column(Integer, nullable=False)
    buzzer_borrow = Column(Integer, nullable=False)
    infared_sensor_borrow = Column(Integer, nullable=False)
    keypad_borrow = Column(Integer, nullable=False)
    led_matrix_borrow = Column(Integer, nullable=False)
    number_led_borrow = Column(Integer, nullable=False)
    photoresistor_borrow = Column(Integer, nullable=False)
    remote_borrow = Column(Integer, nullable=False)
    resistor_borrow = Column(Integer, nullable=False)
    rheostat_borrow = Column(Integer, nullable=False)
    tool_box_borrow = Column(Integer, nullable=False)
    tool_box_tray_borrow = Column(Integer, nullable=False)
    uno_r3_borrow = Column(Integer, nullable=False)
    usb_cable_borrow = Column(Integer, nullable=False)
    ultrasonic_borrow = Column(Integer, nullable=False)
    wire_borrow = Column(Integer, nullable=False)
    potentiometer_borrow = Column(Integer, nullable=False)
    servo_engine_borrow = Column(Integer, nullable=False)
    led_borrow = Column(Integer, nullable=False)
    lcd_borrow = Column(Integer, nullable=False)
    thermistor_borrow = Column(Integer, nullable=False)
    date_time_borrow = Column(DateTime, nullable=False)


class StudentReturn(Base):
    __tablename__ = "student_return"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    student_id = Column(String, nullable=False)
    original_image_return = Column(LargeBinary, nullable=False)
    result_image_return = Column(LargeBinary, nullable=False)
    breadboard_return = Column(Integer, nullable=False)
    button_return = Column(Integer, nullable=False)
    buzzer_return = Column(Integer, nullable=False)
    infared_sensor_return = Column(Integer, nullable=False)
    keypad_return = Column(Integer, nullable=False)
    led_matrix_return = Column(Integer, nullable=False)
    number_led_return = Column(Integer, nullable=False)
    photoresistor_return = Column(Integer, nullable=False)
    remote_return = Column(Integer, nullable=False)
    resistor_return = Column(Integer, nullable=False)
    rheostat_return = Column(Integer, nullable=False)
    tool_box_return = Column(Integer, nullable=False)
    tool_box_tray_return = Column(Integer, nullable=False)
    uno_r3_return = Column(Integer, nullable=False)
    usb_cable_return = Column(Integer, nullable=False)
    ultrasonic_return = Column(Integer, nullable=False)
    wire_return = Column(Integer, nullable=False)
    potentiometer_return = Column(Integer, nullable=False)
    servo_engine_return = Column(Integer, nullable=False)
    led_return = Column(Integer, nullable=False)
    lcd_return = Column(Integer, nullable=False)
    thermistor_return = Column(Integer, nullable=False)
    date_time_return = Column(DateTime, nullable=False)
