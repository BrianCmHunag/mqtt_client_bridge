
import paho.mqtt.publish as publish

#publish.single("paho/test/single", "boo", hostname="mqtt.eclipseprojects.io")
publish.single("client_sub_this_topic", "boo", hostname="127.0.0.1")
