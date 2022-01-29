import os

cmd = 'sudo apt-get -y install python3-pip'
os.system(cmd)

cmd = 'pip3 install face_recognition SpeechRecognition opencv-python paho-mqtt numpy statistics reachy-sdk pyttsx3 gTTS scipy pydub'
os.system(cmd)

#PyAudio-0.2.11-cp37-cp37m-win_amd64.whl 