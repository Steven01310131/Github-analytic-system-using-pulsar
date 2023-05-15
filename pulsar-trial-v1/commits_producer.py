import pulsar
import requests
import json

# Load the token
token="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"
headers = {'Authorization': 'token ' + token}

# Create a pulsar client by supplying ip address and port
client = pulsar.Client('pulsar://localhost:6650')

# Subscribe to a topic and subscription
repo_consumer = client.subscribe('repositories.main', subscription_name='github-sub')

# Create a producers on the topic that consumer can subscribe to
commits_producer = client.create_producer('repositories.commits')
tests_producer = client.create_producer('repositories.tests')
cicd_producer = client.create_producer('repositories.cicd')

while True:
    message = repo_consumer.receive()
    try:
        print("Received message '{}' id='{}'".format(message.data(), message.message_id()))
        repository=json.loads(message.data().decode('utf-8'))

        # INCLUDE CODE TO INSERT / UPDATE IN MONGO

        commits=dict(requests.get(f"https://api.github.com/repos/{repository['full_name']}/commits?per_page=1&page=1").headers)
        commits_producer.send((json.dumps(commits)).encode('utf-8'))
        
        # Acknowledge successful processing of the message
        repo_consumer.acknowledge(message)
    except Exception:
        # Message failed to be processed
        repo_consumer.negative_acknowledge(message)

client.close()