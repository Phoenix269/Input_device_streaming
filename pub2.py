import evdev # lib for getting the list of input devices
import paho.mqtt.publish as publish # MQTT client
#import click #lib for keyboard events
from pynput import keyboard #lib for keyboard
from pynput.mouse import Listener # lib for mouse events
import cv2 #lib for openCV
import os	# lib used to get the current work directory
import base64
import json

MQTT_SERVER = "localhost"
MQTT_PATH = "test_channel"
MQTT_PATH1 = "vid_chan"
MQTT_PATH2 = "dis_chan"
dev_lis=[]

def devstat():
	##### Code to get the device status############
				devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
				for device in devices:
					dev_lis.append(device.name)

				if "SynPS/2 Synaptics TouchPad" in dev_lis:
					publish.single(MQTT_PATH, "MOUSE IS CONNECTED", hostname=MQTT_SERVER)
				else :
					publish.single(MQTT_PATH, "MOUSE IS NOT CONNECTED", hostname=MQTT_SERVER)
				if "AT Translated Set 2 keyboard" in dev_lis:
					publish.single(MQTT_PATH, "KEYBOARD IS CONNECTED", hostname=MQTT_SERVER)
				else :
					publish.single(MQTT_PATH, "KEYBOARD IS NOT CONNECTED", hostname=MQTT_SERVER)
				if "Laptop_Integrated_Webcam_HD: In" in dev_lis:
					publish.single(MQTT_PATH, "CAMERA IS CONNECTED", hostname=MQTT_SERVER)
				else :
					publish.single(MQTT_PATH, "CAMERA IS NOT CONNECTED", hostname=MQTT_SERVER)
				return dev_lis

def devkey():
	#############code to input from keyboard########
				#stdin_text = click.get_text_stream('stdin')
				#for line in stdin_text:
					#publish.single(MQTT_PATH, line, hostname=MQTT_SERVER)

	#########Alternate code to input from keyboard##############
				#while True:
					#pub = raw_input("Type here!!!")
					#if pub == "end":
						#break
					#else:
						#publish.single(MQTT_PATH, pub, hostname=MQTT_SERVER)

	#########Code to stream keyboard##############

	def on_press(key):
	    try:
		#print('alphanumeric key {0} pressed'.format(key.char))
		publish.single(MQTT_PATH, '{0}'.format(key.char), hostname=MQTT_SERVER)
	    except AttributeError:
		#print('special key {0} pressed'.format(key))
		publish.single(MQTT_PATH, '{0}'.format(key), hostname=MQTT_SERVER)

	def on_release(key):
	    #print('{0} released'.format(key))
	    if key == keyboard.Key.esc:
			# Stop listener
			return False

	with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
    	 listener.join()
		listener = keyboard.Listener(on_press=on_press,on_release=on_release)
		listener.start()

def devmo():
	###########code to check an event for mouse#####
				def on_move(x, y):
				    publish.single(MQTT_PATH, "Mouse moved", hostname=MQTT_SERVER)
				    #print("I am here")

				def on_click(x, y, button, pressed):
				    publish.single(MQTT_PATH, "Mouse clicked", hostname=MQTT_SERVER)
				    #print("Click")

				def on_scroll(x, y, dx, dy):
				    publish.single(MQTT_PATH, "Mouse scrolled", hostname=MQTT_SERVER)
				    listener.stop()

				with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
				    listener.join()
def devcam():
	###########code for video streaming#######

				cap = cv2.VideoCapture(0)
				while True:
				    # Capture frame-by-frame
				    ret, frame = cap.read()
				    frame = cv2.resize(frame, (640, 480))
	        		result, buffer = cv2.imencode('.jpg', frame)
				    jpg_as_text = base64.b64encode(buffer)
				    publish.single(MQTT_PATH1, jpg_as_text, hostname=MQTT_SERVER)
				    frame_count = int(cap.get(cv2.CAP_PROP_FPS))
				    #print(frame_count)
				    cv2.imshow('frame',frame)
				    if cv2.waitKey(1) & 0xFF == ord('q'):
					break
				cap.release()
				cv2.destroyAllWindows()



if __name__== "__main__":


	with open('data.txt') as json_file:
	    data = json.load(json_file)
	    dev = []
	    for p in data['selection']:
		print('Selected input: ' + p['sel'])
		if p['sel'] == '1':
			dev = devstat()
		elif (p['sel'] == '2'and "Dell KB216 Wired Keyboard" in dev):
			devkey()
		elif (p['sel'] == '3' and "DELL Laser Mouse" in dev):
			devmo()
		elif (p['sel'] == '4'and "Live! Cam Sync HD VF0770" in dev):
			devcam()
		elif p['sel'] == '5':
			publish.single(MQTT_PATH2, "Disconnecting....", hostname=MQTT_SERVER)
			break
		else:
			print("Wrong Selection!!!")
