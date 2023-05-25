#!/usr/bin/python3
import rospy
from std_msgs.msg import Bool, Float32
import serial
import time
global ultra_1

ultra_1 = 0
ultra_2 = 0
ultra_3 = 0
ultra_4 = 0

arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=.1)

# Callback function for the 'Obstacle' topic
def obstacle1_callback(msg):
    global ultra_1
    # Extract the boolean value from the received message
    ultra_1 = msg.data

def obstacle2_callback(msg):
    global ultra_2
    # Extract the boolean value from the received message
    ultra_2 = msg.data
    
def obstacle3_callback(msg):
    global ultra_3
    # Extract the boolean value from the received message
    ultra_3 = msg.data
    
def obstacle4_callback(msg):
    global ultra_4
    # Extract the boolean value from the received message
    ultra_4 = msg.data

    

# Initialize the ROS node
rospy.init_node('Obstacle_Subscriber')

# Subscribe to the 'Obstacle' topic with the callback function
rospy.Subscriber('Obstacle1', Bool, obstacle1_callback)
rospy.Subscriber('Obstacle2', Bool, obstacle2_callback)
rospy.Subscriber('Obstacle3', Bool, obstacle3_callback)
rospy.Subscriber('Obstacle4', Bool, obstacle4_callback)

pub_mr = rospy.Publisher('wr_set', Float32, queue_size=10)

pub_ml = rospy.Publisher('wl_set', Float32, queue_size=10)
# Keep the node running until shutdown

while (not rospy.is_shutdown()):
    #arduino.write(b'f')
    #time.sleep(2)
    #arduino.write(b's')
    #time.sleep(2)
    #arduino.write(b'l')
    #time.sleep(2)
    #arduino.write(b'r')
    arduino.write(b'f')
    if ultra_2 == 1 or ultra_3 == 1:
        arduino.write(b's')
        time.sleep(5)
        if ultra_1 == 1 and ultra_4 == 1:
            arduino.write(b's')
        elif ultra_1 == 1:
            arduino.write(b'l')
            time.sleep(2)
            arduino.write(b's')
            time.sleep(2)
            arduino.write(b'f')
            time.sleep(2)
            arduino.write(b's')
            time.sleep(2)
            arduino.write(b'r')
            time.sleep(2)
            arduino.write(b's')
            time.sleep(2)
        elif ultra_4 == 1:
            arduino.write(b'r')
            time.sleep(2)
            arduino.write(b's')
            time.sleep(2)
            arduino.write(b'f')
            time.sleep(2)
            arduino.write(b's')
            time.sleep(2)
            arduino.write(b'l')
            time.sleep(2)
            arduino.write(b's')
            time.sleep(2)
        else:
            arduino.write(b'r')
            time.sleep(2)
            arduino.write(b's')
            time.sleep(2)
            arduino.write(b'f')
            time.sleep(2)
            arduino.write(b's')
            time.sleep(2)
            arduino.write(b'l')
            time.sleep(2)
            arduino.write(b's')
            time.sleep(2)
    else:
        arduino.write(b'f')  
        
        
    
    
    
    #if (ultra_2 == 1 or ultra_3 == 1):
     #   arduino.write('s')
    #else:
     #   arduino.write('f')
    
    
    

