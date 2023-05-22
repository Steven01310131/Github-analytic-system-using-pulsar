import pulsar
import json
from pprint import pprint
# Create a pulsar client by supplying ip address and port
client = pulsar.Client('pulsar://192.168.2.43:6650')
data={}
# Subscribe to a topic and subscription
consumer = client.subscribe('Repos2', subscription_name='DE-sub')
#consumer2= client.subscribe('Commits2', subscription_name='DE-sub')
while True:
    msg = consumer.receive(timeout_millis=20000)
    test =  msg.data().decode('utf-8')
    consumer.acknowledge(msg)
    print(test)
client.close()