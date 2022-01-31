import speech_recognition as sr
r = sr.Recognizer()

import paho.mqtt.publish as publish

def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone(device_index=0) as source:
        r.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = r.listen(source, phrase_time_limit=4)
    try:
        input = r.recognize_google(audio)
        print("You said: " + input)
        return str(input)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


while 1:
    publish.single("/reachy", payload=speech_to_text(), qos=0, hostname="13.81.105.139", port=1883)