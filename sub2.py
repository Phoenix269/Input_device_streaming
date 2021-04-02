import paho.mqtt.client as mqtt # MQTT client
import cv2 #lib for openCV
import numpy as np
import base64


MQTT_SERVER = "localhost"
MQTT_PATH = "test_channel"
MQTT_PATH1 = "vid_chan"
MQTT_PATH2 = "dis_chan"


########function to play the saved video###################


def vid_ply(frame):
		img = base64.b64decode(frame)
		npimg = np.fromstring(img, dtype=np.uint8)
		source = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
		cv2.imshow('image',source)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
		return


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH,qos=1)
    client.subscribe(MQTT_PATH1,qos=1)
    client.subscribe(MQTT_PATH2,qos=1)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if (msg.topic) == "vid_chan": #condition to differentiate between the camera and other device feeds
	vid_ply(msg.payload)
    elif (msg.topic) == "dis_chan":
	print(str(msg.payload))
	client.disconnect()
    else:
	print(msg.topic+" "+str(msg.payload))

if __name__== "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_SERVER, 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a manual interface.
    client.loop_forever()
