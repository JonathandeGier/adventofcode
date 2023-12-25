import json
import os

#############################################################################################
#                                                                                           #
#   This script generates a timeline of the leaderboard in csv format                       #
#   1. Put the leaderboard json response in solutions/2023/input/leaderboard.json           #
#   2. run this script                                                                      #
#   3. The csv file will be located at solutions/2023/visuals/leaderboard/leaderboard.csv   #
#                                                                                           #
#############################################################################################


# load the json data
filename = 'solutions/2023/input/leaderboard.json'
try: 
    with open(filename, "r") as f: 
        data = json.loads(f.read()) 
except: 
    raise Exception(f"Reading {filename} file encountered an error") 

# get the timestamps from the stars from each members 
star_completions = []
members = []
for member in data['members'].values():
    members.append(member['name'])

    for day in member['completion_day_level']:
        for part in member['completion_day_level'][day]:
            star_completions.append((member['completion_day_level'][day][part]['get_star_ts'], member['name'], day, part))

# sort by the timestamp
star_completions.sort()

# make the timeline
timeline = []
initial_points = {member:0 for member in members}
initial_points['timestamp'] = 1701406800
timeline.append(initial_points)

star_points = {}
for day in range(1, 26):
    star_points[f'{day}-1'] = len(members)
    star_points[f'{day}-2'] = len(members)

# calculate the new points for each star completion
for timestamp, member, day, part in star_completions:

    points = star_points[f'{day}-{part}']
    star_points[f'{day}-{part}'] -= 1

    new_points = {key:value for key, value in timeline[-1].items()}
    new_points['timestamp'] = timestamp
    new_points[member] += points

    timeline.append(new_points)

# sort the members by the amount of points
members.sort(key=lambda member: timeline[-1][member], reverse=True)

# make directories if they dont exist
path = f'solutions/2023/visuals/leaderboard/leaderboard.csv'
folders = path.split('/')
for i in range(1, len(folders)):
    sub_directory = '/'.join(folders[:i]) + '/'
    if not os.path.isdir(sub_directory):
        os.mkdir(sub_directory)

# Save the timeline in a csv format
with open(path, 'w') as file:
    file.write(f'timestamp,{",".join(members)}\n')
    for entry in timeline:
        file.write(str(entry['timestamp']))
        for member in members:
            file.write(',' + str(entry[member]))
        file.write('\n')