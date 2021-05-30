import requests
import json
import os
import decouple
from decouple import config
import re
from test import send_alert
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from regexx import getPotentialAddresses
from test import writeCSV, readCSVList, emptyCSV
from __init__ import db,User
from datetime import datetime
import os


def write_file(filename, data):
    if os.path.isfile(filename):
        with open(filename, 'a') as f:
            f.write('\n' + data)
    else:
        with open(filename, 'w') as f:
            f.write(data)

# Simple function to get formatted data
def print_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    data = "Current Time = " + current_time
    return data

# Write to text.txt as a log
write_file(
    'test.txt', "<-------------------------------------------------------------------->")
write_file('test.txt', print_time())

# Gets last viewed tweet's ID from CSV file
currSinceID = readCSVList("/root/sinceID.csv")[0]

# Configures Authentication Variables from environment file
API_KEY = config('API_KEY')
API_SECRET = config('API_SECRET')
BEARER_TOKEN = config('BEARER_TOKEN')
ACCESS_TOKEN = config('ACCESS_TOKEN')
ACCESS_SECRET = config('ACCESS_SECRET')


# Authorization method
def auth():
    return BEARER_TOKEN

# Returns formatted URL to access twitter API url
def create_url(currSinceID):

    url = f'https://api.twitter.com/2/tweets/search/recent?query=from:1373531468744552448&since_id={currSinceID}&tweet.fields=created_at,in_reply_to_user_id,source,referenced_tweets&max_results=20'
    return(url)

#Returns header to accompany API call
def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


# Makes request to API and gets the actual tweets
def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


# Authenticates and gets json response(all the tweets)
bearer_token = auth()
url = create_url(currSinceID)
headers = create_headers(bearer_token)
json_response = connect_to_endpoint(url, headers)

# Gets reference to users in result list
result = []
for i in users:
    result.append(f'{i.name}|{i.location}|{i.phonenumber}|{i.age}')

# Gets reference to all unique locations in locations list
locations = []
for i in users:
    if i.location not in locations:
        locations.append(i.location)

#Initializes sendOutDict (keeps track of all the messages that will need to be sent) and coutner
sendOutDict = {}
counter = 0

#Checks if json_response contains data/response from twitterAPI came back as expected
if 'data' in json_response:
    #Loops thru each tweet in jsonReponse
    for x in json_response['data']:

        #If counter is 0/set new sinceID
        if counter == 0:
            since_id = x['id']
            emptyCSV("/root/sinceID.csv")
            writeCSV("/root/sinceID.csv", since_id)
        #Increment counter
        counter += 1

        #Find all locations detected in tweets text
        locationsFound = getPotentialAddresses(x['text'], locations)

        #Loops thru each location in locations found
        for locationFound in locationsFound:
            # If location is already in sendOutDict -> Append to it
            if locationFound in sendOutDict:
                sendOutDict[locationFound].append(x["text"]+"|||||"+x['id'])
            #Else-> Create new list under sendOutDict[locationFound]
            else:
                sendOutDict[locationFound] = [x['text']+"|||||"+x['id']]


# Loop through list of all users
prin
for i, person in enumerate(result):
    # Get and organize user info
    info = result[i].split('|')
    name = info[0]
    location = info[1]
    phonenumber = info[2]
    age = info[3]
    write_file("test.txt", f"{i} --- {info}")

    for x in sendOutDict.keys():

        # print(x, len(sendOutDict[x]))
        # print("------------------")

        if x != location:
            continue

        for i in sendOutDict[x]:
            text = i.split('|||||')[0]
            tweetID = i.split('|||||')[1]
            write_file("test.txt", f"TWEET: {text} \n ID: ---- {tweetID}")
            # print("TEXT", text.encode("utf-8"))
            # write_file('test.txt' , "TEXT" + text)
            # print("ID", tweetID.encode("utf-8"))
            # write_file('test.txt' , "ID" + tweetID)
            send_alert(name, phonenumber, location, age, text)
            print(
                f"{name} | | | {phonenumber} | | | {location} | | | {age} | | | {text}")

        print("")
        print("")


# print('end')

#send_alert("Ahmed", "16477464125", "location", "age", "text")

write_file('test.txt', "END")
write_file(
    'test.txt', "<-------------------------------------------------------------------->")
write_file(
    'test.txt', "<-------------------------------------------------------------------->")
write_file(
    'test.txt', "<-------------------------------------------------------------------->")
