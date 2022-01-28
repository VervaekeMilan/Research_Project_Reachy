# class Move_body():

#     def __init__():
#         self.object
    #Turn off

from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory.interpolation import InterpolationMode

reachy = ReachySDK(host='127.0.0.1')

import face_recognition as fr
import cv2

import time
    
def load_vars():
    #VARIABLES
    r_gripper = 0
    l_gripper = 0

    l_shoulder_p = 0
    l_shoulder_r = 30
    l_arm_y = -40
    l_elbow_p = -90
    l_forearm_y = -90
    l_wrist_p = -20    
    l_wrist_r = 40   

    r_shoulder_p = 0
    r_shoulder_r = -30
    r_arm_y = 40
    r_elbow_p = -90
    r_forearm_y = 90
    r_wrist_p = -20    
    r_wrist_r = -40   


def adjust_head():
    head_position = {
        reachy.head.joints.l_antenna: -2.49,
        reachy.head.joints.r_antenna: -0.44,
        reachy.head.joints.neck_disk_top: -54.72,
        reachy.head.joints.neck_disk_middle: -69.77,
        reachy.head.joints.neck_disk_bottom: -54.11,
    }
    move(head_position)

#Hand + arm to desired pos for project
def adjust_r_pos():
    right_angled_position = {
        reachy.r_arm.r_shoulder_pitch: r_shoulder_p,
        reachy.r_arm.r_shoulder_roll: r_shoulder_r,
        reachy.r_arm.r_arm_yaw: r_arm_y,
        reachy.r_arm.r_elbow_pitch: r_elbow_p,
        reachy.r_arm.r_forearm_yaw: r_forearm_y,
        reachy.r_arm.r_wrist_pitch: r_wrist_p,
        reachy.r_arm.r_wrist_roll: r_wrist_r,
    }
    #print(r_gripper)
    move_r_hand(r_gripper)
    move_r_arm(right_angled_position)

#Hand + arm to desired pos for project
def adjust_l_pos():
    left_angled_position = {
    reachy.l_arm.l_shoulder_pitch: l_shoulder_p,
    reachy.l_arm.l_shoulder_roll: l_shoulder_r,
    reachy.l_arm.l_arm_yaw: l_arm_y,
    reachy.l_arm.l_elbow_pitch: l_elbow_p,
    reachy.l_arm.l_forearm_yaw: l_forearm_y,
    reachy.l_arm.l_wrist_pitch: l_wrist_p,
    reachy.l_arm.l_wrist_roll: l_wrist_r,
    }
    move_l_hand(l_gripper)
    move_l_arm(left_angled_position)

def move(pos):
    goto(
        goal_positions=pos,
        duration=1.0,
        interpolation_mode=InterpolationMode.MINIMUM_JERK
        )

#move gripper
def move_r_hand(value):
    if(value=='open'): value = -20
    if(value=='close'): value = 20
    r_gripper = value
    print(r_gripper)
    reachy.turn_on('r_arm')
    gripper = {
        reachy.r_arm.r_gripper: r_gripper #(20 --> CLOSE / -20 --> OPEN)
    }
    move(gripper)

#move gripper
def move_l_hand(value):
    if(value=='open'): value = 20
    if(value=='close'): value = -20
    l_gripper = value
    reachy.turn_on('l_arm')
    gripper = {
        reachy.l_arm.l_gripper: l_gripper #(-20 --> CLOSE / 20 --> OPEN)
    }
    move(gripper)

#Move right arm
def move_r_arm(pos):
    reachy.turn_on('r_arm')
    move(pos)

#Move left arm
def move_l_arm(pos):
    reachy.turn_on('l_arm')
    move(pos)

#rest right arm
def rest_r():
    reachy.turn_off_smoothly('r_arm')

def rest_l():
    reachy.turn_off_smoothly('l_arm')

def rest_head():
    reachy.turn_off_smoothly('head')

def shutdown():
    rest_head()
    rest_l()
    rest_r()   
    
def get_player_amount():
  video_capture = reachy.left_camera
  frame = video_capture.last_frame
  rgb_frame = frame[:, :, ::-1]
  face_locations = fr.face_locations(rgb_frame)
  return(len(face_locations))   
    
 

