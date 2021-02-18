import time as t
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import sensor

ENDPOINT = "ao9qxmwglcuca-ats.iot.eu-central-1.amazonaws.com"
CLIENT_ID = "54dddebc-a706-4439-8fc4-bb8b41a6b4e4"
PATH_TO_CERT = "certificates/34686ff72b-certificate.pem.crt"
PATH_TO_KEY = "certificates/34686ff72b-private.pem.key"
PATH_TO_ROOT = "certificates/root.pem"
TOPIC = "pool-temperature"

myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)

myAWSIoTMQTTClient.connect()

temp = sensor.read_temp()
message = {"sensorId": "pool_temp_1", "sensor_value": temp, "timestamp": round(t.time() * 1000)}
myAWSIoTMQTTClient.publish(TOPIC, json.dumps(message), 1)
myAWSIoTMQTTClient.disconnect()