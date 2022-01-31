from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory.interpolation import InterpolationMode

reachy = ReachySDK(host='127.0.0.1')


import face_recognition as fr
import cv2
import time
import numpy as np
from statistics import mean

from reachyAudio import reachyAudio
reachy_audio = reachyAudio.ReachyAudio() #Get audio ready

#VARIABLES
# r_gripper = 0
# l_gripper = 0

# l_shoulder_p = 0
# l_shoulder_r = 30
# l_arm_y = -40
# l_elbow_p = -90
# l_forearm_y = -90
# l_wrist_p = -20    
# l_wrist_r = 40   

# r_shoulder_p = 0
# r_shoulder_r = -30
# r_arm_y = 40
# r_elbow_p = -90
# r_forearm_y = 90
# r_wrist_p = -20    
# r_wrist_r = -40


#VARIABLES
locations = []

#movements
reach = np.array([
    [-0.27439431, -0.1039175 , -0.95598584,  0.43870858],
       [-0.96111198,  0.06186045,  0.2691413 ,  0.17362613],
       [ 0.03116922,  0.99266028, -0.11685051, -0.25943446],
       [ 0.        ,  0.        ,  0.        ,  1.        ]
])
hold = np.array([
[-0.93041691, -0.07393605, -0.35896772,  0.30971189],
       [-0.35692519, -0.03965655,  0.93329083,  0.27420855],
       [-0.08323926,  0.99647419,  0.01050748, -0.1504515 ],
       [ 0.        ,  0.        ,  0.        ,  1.        ]
])
hold_close = np.array([
    [-0.96804607, -0.08284013, -0.23669455,  0.15796007],
       [-0.22514398, -0.12857312,  0.96580492,  0.10111066],
       [-0.11043996,  0.98823401,  0.10581375, -0.18974673],
       [ 0.        ,  0.        ,  0.        ,  1.        ]
])

hello = np.array([
       [ 0.82616696, -0.53814508, -0.1668773 ,  0.18156075],
       [-0.55640603, -0.73266007, -0.39194585,  0.36205863],
       [ 0.0886594 ,  0.41666424, -0.90472671,  0.1012273 ],
       [ 0.        ,  0.        ,  0.        ,  1.        ]
])

distribute_r = np.array([
    [-0.65080684,  0.35368236, -0.67183275,  0.34993856],
       [ 0.74795881,  0.14666872, -0.64733755, -0.08691086],
       [-0.13041503, -0.92379493, -0.35999284, -0.21705775],
       [ 0.        ,  0.        ,  0.        ,  1.        ]]
)

def change_value(position):
    print(f"changing value: {position}")
    right = np.array([
        [ 0.46029321, -0.43133549, -0.77593805,  0.32500746],
           [ 0.87220499,  0.38265532,  0.30468568, position],
           [ 0.16549508, -0.81702179,  0.55234661, -0.47046282],
           [ 0.        ,  0.        ,  0.        ,  1.        ]
    ])
    left = np.array([
        [-0.73426003, -0.45913322, -0.50005889,  0.25496351],
           [ 0.66852527, -0.36093785, -0.65022906,  position],
           [ 0.11805158, -0.81173922,  0.57196439, -0.48427583],
           [ 0.        ,  0.        ,  0.        ,  1.        ]
    ])
    return left, right


def move_inv(value):
    if value == "left":
        reachy.turn_on('r_arm')
        joint_pos_dis= reachy.r_arm.inverse_kinematics(left)
    elif value == "right":
        reachy.turn_on('l_arm')
        joint_pos_dis= reachy.r_arm.inverse_kinematics(right)       
    goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), joint_pos_dis)}, duration=1.0)
    

def adjust_head():
    reachy.turn_on('head')
    head_position = {
        reachy.head.joints.l_antenna: -2.49,
        reachy.head.joints.r_antenna: -0.44,
        reachy.head.joints.neck_disk_top: -54.72,
        reachy.head.joints.neck_disk_middle: -69.77,
        reachy.head.joints.neck_disk_bottom: -54.11,
    }
    move(head_position)

#Hand + arm to desired pos for project
"""def adjust_r_pos(r_shoulder_p = 0, r_shoulder_r = -30, r_arm_y = 40, r_elbow_p = -90, r_forearm_y = 90, r_wrist_p = -20, r_wrist_r = -40, r_gripper = 0):
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
    move_r_arm(right_angled_position)"""
    
def adjust_r_pos_kin(command):
    if command == 'distribute':
        joint_pos_dis= reachy.r_arm.inverse_kinematics(distribute_r)
        
        reachy.turn_on('r_arm')
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), joint_pos_dis)}, duration=2.0)
        head_follow_hand()

def adjust_r_pos_kin2(pos):
    left, right = change_value(pos)
    if pos < -0.16:
        reachy.turn_on('r_arm')
        joint_pos_dis= reachy.r_arm.inverse_kinematics(right)   
    else:
        reachy.turn_on('r_arm')
        joint_pos_dis= reachy.r_arm.inverse_kinematics(left)

    goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), joint_pos_dis)}, duration=1.0)
    head_follow_hand()

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
        reachy.l_arm.l_gripper: l_gripper #(-20 --> CLOSE / 20 --> )
    }
    move(gripper)
    
#Hand + arm to desired pos for project
"""def adjust_l_pos(l_shoulder_p = 0, l_shoulder_r = 30, l_arm_y = -40, l_elbow_p = -90, l_forearm_y = -90, l_wrist_p = -20, l_wrist_r = 40, l_gripper = 0):
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
    move_l_arm(left_angled_position)"""
    
def adjust_l_pos_kin(command):
    if command == 'reach':
        joint_pos_reach = reachy.l_arm.inverse_kinematics(reach)

        reachy.turn_on('l_arm')
        goto({joint: pos for joint,pos in zip(reachy.l_arm.joints.values(), joint_pos_reach)}, duration=1.0)
    if command == 'hold':
        #move_l_hand("open")
        joint_pos_reach = reachy.l_arm.inverse_kinematics(hold)

        reachy.turn_on('l_arm')
        goto({joint: pos for joint,pos in zip(reachy.l_arm.joints.values(), joint_pos_reach)}, duration=1.0)
    if command == 'hold_close':
        joint_pos_reach = reachy.l_arm.inverse_kinematics(hold_close)
        reachy.turn_on('l_arm')
        goto({joint: pos for joint,pos in zip(reachy.l_arm.joints.values(), joint_pos_reach)}, duration=1.0)
    if command == 'hello':
        joint_pos_reach = reachy.l_arm.inverse_kinematics(hello)
        reachy.turn_on('l_arm')
        goto({joint: pos for joint,pos in zip(reachy.l_arm.joints.values(), joint_pos_reach)}, duration=1.0)
    

def move(pos):
    goto(
        goal_positions=pos,
        duration=1.0,
        interpolation_mode=InterpolationMode.MINIMUM_JERK
        )

#Move right arm
def move_r_arm(pos):
    reachy.turn_on('r_arm')
    move(pos)

#Move left arm
def move_l_arm(pos):
    reachy.turn_on('l_arm')
    move(pos)
    
def move_antenna(value):
    reachy.turn_on('head')
    reachy.head.l_antenna.goal_position = value
    reachy.head.r_antenna.goal_position = value

#rest right arm
def rest_r():
    reachy.turn_off_smoothly('r_arm')

def rest_l():
    reachy.turn_off_smoothly('l_arm')

def rest_head():
    reachy.turn_off_smoothly('head')
    
    
def head_follow_hand():
    try:
        reachy.turn_on('head')

        x, y, z = reachy.r_arm.forward_kinematics()[:3,-1] # We want the translation part of Reachy's pose matrix
        reachy.head.look_at(x=x, y=y, z=z-0.05, duration=1.0) # There is a 5cm offset on the z axis
    except: print("Reachy's hand is out of range")

def shutdown():
    #rest_head()
    rest_l()
    rest_r()
    toggle_fans(0)
    move_antenna(0)

#class camera():
def get_middle(locations):
    values = []
    for location in locations:
        values.append(int(mean((location[1],location[3]))))
    return values

def get_player_amount():
  video_capture = reachy.right_camera
  print(video_capture)
  frame = video_capture.last_frame
  rgb_frame = frame[:, :, ::-1]
  face_locations = fr.face_locations(rgb_frame)
  if len(face_locations) != None:
      return(len(face_locations), get_middle(face_locations))
  else: return(len(face_locations), None)
    
def toggle_fans(boolean):
    for motor, fan in reachy.fans.items():
       if boolean == 1: fan.on()
       else: fan.off()

def confirm_players():
    print("confirm")
    global locations
    print(locations)
    amount, locations = get_player_amount()
    print(amount)
    if amount == 0: confirm_players()
    elif amount > 3: 
        reachy_audio.speak(f"Sorry, I see more than 3 players")
        confirm_players()
    elif amount == 1:
        reachy_audio.speak(f"I can count {amount} player, is that right?")
    else: reachy_audio.speak(f"I can count {amount} players, is that right?")
    return(True)
    
    
def distribute():
    reachy_audio.speak("Let's begin, shall we!")
    #functions.adjust_l_pos_kin("hold")
    print("distribute")
    dist_pos = []
    global locations
    if len(locations) == 1: dist_pos.append(0.15)
    elif len(locations) == 2: 
        dist_pos.append(0.15)
        dist_pos.append(-0.45)
    elif len(locations) == 3:
        dist_pos.append(-0.20)
        dist_pos.append(0.15)
        dist_pos.append(-0.45)
    #for location in locations:
    adjust_l_pos_kin("hold_close")
    for number in range(5):
        print("moving")
        for pos in dist_pos:
            print("ready")
            time.sleep(1)
            move_r_hand("close")
            adjust_r_pos_kin2(pos)
            
            time.sleep(0.5)
            move_r_hand("open")
            adjust_r_pos_kin('distribute')
    adjust_head()
    reachy_audio.speak("I guess this was enough dealing for our demo")
    move_antenna(20)
    time.sleep(1)
    move_antenna(0.8)
    reachy_audio.speak("Just say start again if I should continue dealing the cards")
