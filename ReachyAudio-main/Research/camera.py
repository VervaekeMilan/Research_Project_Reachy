import face_recognition as fr
import cv2

#class camera():

def get_player_amount(reachy):
  frame = video_capture.last_frame
  rgb_frame = frame[:, :, ::-1]
  face_locations = fr.face_locations(rgb_frame)
  return(len(face_locations))