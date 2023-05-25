#!/usr/bin/env python3

import cv2
import rospy
from std_msgs.msg import Int32
import time 
import serial

cap = cv2.VideoCapture(0)
fire_detector = cv2.CascadeClassifier("/home/pi/ros_catkin_ws/src/fire_fighter/src/fire_detection.xml")
fire_pub = rospy.Publisher('fire_detection', Int32, queue_size=10)
rospy.init_node('fire_detection_node', anonymous=True)
publish_rate = rospy.Rate(1)  # 1 message per second
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)
while not rospy.is_shutdown():
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip image horizontally
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    fire = fire_detector.detectMultiScale(img, 1.2, 5)
    fire_detected = 0
    fire_area = 0
    image_area = img.shape[0] * img.shape[1]
    
    for (x, y, w, h) in fire:
        if y + h < img.shape[0] // 2:  # Check if the fire is in the upper part of the image
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3)
            rospy.loginfo("Fire Detected in the upper part")
            fire_detected = 2
            fire_area += w * h
        else:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            rospy.loginfo("Fire Detected in the lower part")
            fire_detected = 1
            fire_area += w * h
    if fire_detected == 0:
        arduino.write(b'A')
    elif fire_detected == 1:
        arduino.write(b'B')
    elif fire_detected == 2:
        arduino.write(b'C')
    #if fire_detected == 1 or fire_detected == 1:
    #    time.sleep(2)
    fire_percentage = (fire_area / image_area) * 100
    print(fire_percentage)
    if fire_percentage >= 5.0:
        arduino.write(b'D')
    cv2.imshow('img', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    publish_rate = rospy.Rate(1)  # 1 message per second

cap.release()
cv2.destroyAllWindows()
