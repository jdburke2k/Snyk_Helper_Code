#
# Snyk helper code.
# Author: JD Burke
#
# ********              V1 API               ********
# ******** this will need to be ported to v3 ********
#
#
# Best effort - No promises, help or guarantees should be read into this or expected.
# If you don't like what it does...build your own, or modify the stuff below.
#
# What it does:
# Takes a Group ID and API token and dumps info for the orgs of that group,
# specifically, dumps the username and email and the orgs that user is a member of
# If it is a service account the email returns as None
#
#
import requests
import json
import csv
import time

# # Your Snyk API token
# API_TOKEN = "your-api-token-here"
#
# # Your Group ID
# GROUP_ID = "your-group-token-here"
#


BASE_URL = "https://api.snyk.io/v1/"

# Headers for Snyk API requests
HEADERS = {
    "Authorization": f"token {API_TOKEN}",
    "Content-Type": "application/json",
}

#
# gets info for whatever Group ID you used
group_url = f"{BASE_URL}group/{GROUP_ID}/members"
group_response = requests.get(group_url, headers=HEADERS, timeout=30.0)
group_data = group_response.json()

for member in group_data:
    print(str(member['username'])+' ['+str(member['email'])+']')
    for orgs in member['orgs']:
        print("\t"+orgs['name'])
    print()

    timestr = time.strftime('%Y%m%d-%H%M%S')
    fnout = 'Snyk-ListUsers-' + timestr
    with open(fnout + '.json', 'w') as f:
        json.dump(group_data, f)
        # Open a csv file for writing
        data_file = open(fnout + '.csv', 'w')
        csv_writer = csv.writer(data_file)

        count = 0
        for i in group_data:
            if count == 0:
                # Writing headers of CSV file
                header = i.keys()
                csv_writer.writerow(header)
                count += 1

            csv_writer.writerow(i.values())

        data_file.close()