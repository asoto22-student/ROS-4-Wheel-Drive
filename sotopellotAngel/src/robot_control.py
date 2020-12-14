#!/usr/bin/env python3

import os
import rospy
import numpy as np

from gazebo_msgs.srv import ApplyJointEffort
from gazebo_msgs.srv import GetJointProperties
from geometry_msgs.msg import Twist
from std_msgs.msg import Header

# Constants
MOVE_SPEED = 10
ANGULAR_SPEED = 15
PUB_FREQ = 10
START_TIME = rospy.Time(0, 0)
END_TIME = rospy.Time(0.1/PUB_FREQ, 0)

# Error Gain
k = 7.5

# Global Variables
l_target = 0
r_target = 0

# Name Constants
robot_name = "fw_robot"
seperator = "::"
wheel_dict = ["f_left", "f_right", "b_left", "b_right"]
wheel_hinge = "_wheel_hinge"

# Ros Services
apply_effort = rospy.ServiceProxy('/gazebo/apply_joint_effort', ApplyJointEffort)
get_effort = rospy.ServiceProxy('/gazebo/get_joint_properties',GetJointProperties)

def getValues(msg):
    global l_target, r_target
    dd = getDesRate(msg.linear.x, msg.linear.y)

    l_target = dd[0]
    r_target = dd[1]

    #print(l_target, r_target)

sub = rospy.Subscriber('/cmd_vel', Twist, getValues)

def getRate(wheel_num):
    buff = GetJointProperties()
    buff.joint_name = robot_name + seperator + wheel_dict[wheel_num] + wheel_hinge
    val = get_effort(buff.joint_name)

    #print("Wheel", wheel_dict[wheel_num], "Effort:", val.rate[0])

    return val.rate[0]

def getDesRate(x, y):
    x *= ANGULAR_SPEED
    y *= MOVE_SPEED
    v = (1.0 - np.abs(x)) * y + y
    w = (1.0 - np.abs(y)) * x + x

    wheel_r = (v + w) / 2.0
    wheel_l = (v - w) / 2.0

    return [wheel_l, wheel_r]

def setEffort(wheel_num, effort_amount):
    wheel_name = robot_name + seperator + wheel_dict[wheel_num] + wheel_hinge
    apply_effort(wheel_name, effort_amount, START_TIME, END_TIME)

def moveWheel(wheel_num, target_effort):
    a = getRate(wheel_num)
    e = target_effort - a
    c = e * k
    setEffort(wheel_num, c)

def main():
    rospy.init_node('fw_control')
    rate = rospy.Rate(PUB_FREQ)

    while not rospy.is_shutdown():
        moveWheel(0, l_target)
        moveWheel(1, r_target)
        moveWheel(2, l_target)
        moveWheel(3, r_target)

        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
