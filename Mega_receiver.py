#!/usr/bin/python3
import serial
import rospy
from std_msgs.msg import Int32,Bool
import time

global ser
def fire_callback(msg):
    global ser
    fire_status = msg.data
    if fire_status == 2:
        character =  2
    elif fire_status == 1:
        character =  1
    elif fire_status == 0:
        character =  0
    ser.write(bytes(str(character), 'utf-8'))  # Send the character as a byte
    print(character)
    
# Establish serial communication
ser = serial.Serial('/dev/ttyACM1', 9600)  # Replace '/dev/ttyUSB0' with your Raspberry Pi's serial port
# Initialize the ROS node
rospy.init_node('Obstacle_Detected', anonymous=True)

# Create a publisher with topic name 'threshold'
pub_obs1 = rospy.Publisher('Obstacle1', Bool, queue_size=10)
pub_obs2 = rospy.Publisher('Obstacle2', Bool, queue_size=10)
pub_obs3 = rospy.Publisher('Obstacle3', Bool, queue_size=10)
pub_obs4 = rospy.Publisher('Obstacle4', Bool, queue_size=10)

# Set the threshold value
Max_Distance = 50  # Replace with your desired threshold value

# Your logic to check the threshold
rate = rospy.Rate(10)  # Publish at 10 Hz
while not rospy.is_shutdown():
    # Read data from Arduino
    if ser.in_waiting > 0:
        line = ser.readline()
        data = line.decode('utf-8').rstrip()
        #print(data)
        
        # Check the condition for threshold
        if data == "C": #Close
            pub_obs1.publish(True)  # Publish 'True' when threshold is met
        elif data == "F":
            pub_obs1.publish(False)  # Publish 'False' when threshold is not met
        elif data == "V": #Close
            pub_obs2.publish(True)  # Publish 'True' when threshold is met
        elif data == "G":
            pub_obs2.publish(False)  # Publish 'False' when threshold is not met
        elif data == "B": #Close
            pub_obs3.publish(True)  # Publish 'True' when threshold is met
        elif data == "H":
            pub_obs3.publish(False)  # Publish 'False' when threshold is not met
        elif data == "N": #Close
            pub_obs4.publish(True)  # Publish 'True' when threshold is met
        elif data == "I":
            pub_obs4.publish(False)  # Publish 'False' when threshold is not met
    rospy.Subscriber('fire_detection', Int32, fire_callback)
    rate.sleep()
    

# Close the serial connection
ser.close() 
