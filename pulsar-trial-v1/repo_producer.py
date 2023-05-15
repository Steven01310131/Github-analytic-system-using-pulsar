import pulsar
import requests
import json
from dates_generator import generate_dates

# Load the token
token="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"
headers = {'Authorization': 'token ' + token}

# Create a pulsar client by supplying ip address and port
client = pulsar.Client('pulsar://localhost:6650')

# Create a producer on the topic that consumer can subscribe to
repo_producer = client.create_producer('repositories.main')

# Generate the date values array
dates = generate_dates()

items = []

for day in range(2): # The range can be changed in between 0 and 365 based on the date range we want to extract data
    for i in range(11): # Taking into account that 10% of the repositories have "language": null
        url=f"https://api.github.com/search/repositories?q=created:{date_array[day]}+archived:false&per_page=100&page={i}"
        repositories = requests.get(url,headers=headers).json()
        for item in repositories['items']:
            if(item["language"] is not None):
                trimmed_item = {key: item[key] for key in ["id", "full_name", "created_at", "updated_at", "language"]}
                # json.dumps makes the object to string so we can encode it and send it 
                repo_producer.send((json.dumps(trimmed_item)).encode('utf-8'))

                """Load to items to test if needed"""
                # items.append(trimmed_item)

"""Print first 10 items from items array for testing purposes"""
# print([items[i] for i in range(10)])

# Destroy pulsar
client.close()