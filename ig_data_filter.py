import json
from pathlib import Path
import webbrowser

data_store_location = Path('tharindus609_20230720')

# Load followers file
follower_file_path = Path.joinpath(data_store_location,'followers_and_following/followers_1.json')

followers_json = json.load(open(follower_file_path))

follow_list = []
for follower in followers_json:
    follow_list.append(follower['string_list_data'][0]['value'])

print("total follower count: {0}".format(len(follow_list)))

# load following file
following_file_path = Path.joinpath(data_store_location,'followers_and_following/following.json')

following_json = json.load(open(following_file_path))['relationships_following']

following_list = []
for following in following_json:
    following_list.append(following['string_list_data'][0]['value'])
    if following['string_list_data'][0]['value'] not in follow_list:
        print("not a follower: {0}".format(following['string_list_data'][0]['href']))
        webbrowser.open(following['string_list_data'][0]['href'])

for follower in followers_json:
    if follower['string_list_data'][0]['value'] not in following_list:
        print("not following back: {0}".format(follower['string_list_data'][0]['href']))
        webbrowser.open(follower['string_list_data'][0]['href'])