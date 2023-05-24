import pulsar
import json
import requests
from pprint import pprint
import pymongo
token="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" 
headers = {'Authorization': 'token ' + token}
myclient = pymongo.MongoClient("mongodb://root:example@192.168.2.51:27017/")
mydb = myclient["mydatabase_test"]
mycol = mydb["repositories_test"]
# Create a pulsar client by supplying ip address and port
client = pulsar.Client('pulsar://192.168.2.51:6650')
data={}
# Subscribe to a topic and subscription
consumer1 = client.subscribe('repositories_testtest3', subscription_name='question2')
i_backwards = 49
num_commits = 0
while True:
    msg1= consumer1.receive()
    repo_name=msg1.data().decode('utf-8')
    # commits=requests.get(f"https://api.github.com/repos/{repo_name}/commits?per_page=1&page=1") # without token 
    r = requests.get(f"https://github.com/{repo_name}")
    commits_index = r.text.find("Commits")
    i = commits_index - i_backwards
    commits_str = ""
    commits_magnitude = 0
    c = r.text[i]
    # Unlikely that nr of commits reach 10^6
    while c != '>' and commits_magnitude < 6:
        commits_str = c + commits_str
        i -= 1
        c = r.text[i]
        commits_magnitude += 1
    try:
        num_commits = int(commits_str)
    except:
        print(f"failure for {repo_name}") #TODO remove after testing
        continue

    filter = {
        "full_name": repo_name
    }

    update = {
        "$set": {
            "commits": commits_str
        }
    }

    result = mycol.update_one(filter, update)

    print("Matched:", result.matched_count)
    print("Modified:", result.modified_count)


    
    ###this is for checking that the connect
    data[f'{repo_name}']=num_commits
    print(f"{repo_name} {data[f'{repo_name}']} ")
client.close()