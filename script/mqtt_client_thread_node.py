#!/usr/bin/env python
import paho.mqtt.client as mqtt
import rospy
import threading
from std_msgs.msg import String

class MQTTClient (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        rospy.init_node('mqtt_client', anonymous=False)
        self._ip = rospy.get_param("~ip", default="127.0.0.1")
        self._port= rospy.get_param("~port", default=1883)
        self._send_topic= rospy.get_param("~client_pub_to_this_topic", default="client_pub_to_this_topic") 
        self._reveive_topic= rospy.get_param("~client_sub_this_topic", default="client_sub_this_topic")

        # ros sub/pub
        pub = rospy.Publisher('~receive_message_from_broker', String, queue_size=10) 
        rospy.Subscriber("~send_message_to_broker", String, self.callback) 

        # mqtt client connect cb
        def on_connect(client, userdata, flags, rc):
            rospy.loginfo("MQTT connected with result code "+str(rc))
            client.subscribe(self._reveive_topic)

        # mqtt client sub + ros pub
        # mqtt client sub cb, only works if client.loop_forever()
        def on_message(client, userdata, msg): 
            # rospy.loginfo(msg.topic+" "+str(msg.payload))
            pub.publish(str(msg.payload)) # ros pub
            
        self.client = mqtt.Client() # mqtt client sub/pub
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        try:
            self.client.connect(self._ip, self._port, 60)
        except Exception as e:
            rospy.logerr("{}: {}".format(rospy.get_name(),e)) # Connect error

        self.start()

    # ros sub + mqtt client pub
    # rob sub cb
    def callback(self, data):
        # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        self.client.publish(self._send_topic, data.data) # mqtt client pub


    def run(self):
        self.client.loop_forever()

if __name__ == '__main__':
    try:
        matt_client = MQTTClient()
        rospy.spin()
        matt_client.client.disconnect()
        matt_client.join()

    except Exception as e:
        rospy.logerr("{}".format(e))
        