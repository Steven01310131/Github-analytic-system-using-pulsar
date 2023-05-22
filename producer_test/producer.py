import pulsar
import requests
import json
from pprint import pprint
from requests.structures import CaseInsensitiveDict
# Create a pulsar client by supplying ip address and port
client = pulsar.Client('pulsar://localhost:6650')
# Create a producer on the topic that consumer can subscribe to
producer_1 = client.create_producer('Repos2')
test = "buh" 
producer_1.send(test.encode('utf-8'))

# Destroy pulsar
client.close()