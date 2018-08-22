import os
import json
from time import sleep

file_name = "chores.json"


# create file if it does not exist
if not os.path.isfile(file_name):
    f = open(file_name, "w")
    f.close()

# get time file was last modified
o_time = os.stat(file_name).st_mtime
with open(file_name) as file:
    chores = json.load(file)
    for c in chores['chores']:
        print("Chore: %-20s Assigned to: %10s Is Finished: %-5s" % (
        c['chore'] + ",", c['assignedTo'] + ",", c['finished']))

while True:
    n_time = os.stat(file_name).st_mtime
    if n_time != o_time:
        with open(file_name) as file:
            chores = json.load(file)
            for c in chores['chores']:
                print("Chore: %-20s Assigned to: %10s Is Finished: %-5s" % (
                c['chore'] + ",", c['assignedTo'] + ",", c['finished']))

        o_time = n_time

    if os.stat(file_name).st_size == 0:
        with open(file_name, "w") as f:
            data = {'chores': []}
            data['chores'].append({
                'chore': "Pet cats",
                'assignedTo': "Greg",
                'finished': 'false'
            })
            data['chores'].append({
                'chore': "water plants",
                'assignedTo': "Alex",
                'finished': 'false'
            })
            json.dump(data, f)

    sleep(12)