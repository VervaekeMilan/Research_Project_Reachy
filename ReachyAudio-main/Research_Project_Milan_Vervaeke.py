from Research import functions
import time


from paho.mqtt import client as mqtt
from reachyAudio import reachyAudio

functions.shutdown() #Shutdown
functions.toggle_fans(1) #Turn of so it can adjust to ambient noise
reachy_audio = reachyAudio.ReachyAudio()

functions.toggle_fans(1)

#reachy_audio.speak("Hello, my name is Reachy. Please hand me the cards so I can start dealing")
functions.adjust_head()
reachy_audio.speak("Hello, I'm reachy. Please give me the tray so we can begin")
functions.adjust_l_pos_kin("reach")
functions.move_l_hand("open")


#Variables
confirm = False
            
def on_connect(client, userdata, flags, rc):
    client: mqtt.Client
    client.subscribe("/reachy")
    
def on_message(client, userdata, msg): 
    global confirm
    text = ((str(msg.payload, "utf-8")).replace("'", "").replace("b", "")).lower() 
    if "close" in text: functions.move_l_hand(-12)
    if "open" in text: functions.move_l_hand("open")
    if "start" in text:
        functions.move_l_hand(-12)
        functions.adjust_l_pos_kin("hold")
        functions.adjust_r_pos_kin('distribute')
        confirm =  functions.confirm_players()
        
    if "sleep" in text: functions.shutdown()
    if "thank" in text: reachy_audio.speak("It's my pleasure to serve you human.")

    print(f"text: {text}")
    if "die" in text: functions.rest_head()
    if "wake" in text: functions.adjust_head()
    
    if "yes" in text: 
        if confirm == True:
            functions.distribute()
            confirm = False
    if "no" in text:
        if confirm == True:
            confirm = False
            confirm = functions.confirm_players()

            
#MQTT        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("13.81.105.139", 1883, 60)
client.loop_forever(10)




