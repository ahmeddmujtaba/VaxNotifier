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


from datetime import datetime
import os
 
def write_file(filename,data):
    if os.path.isfile(filename):
        with open(filename, 'a') as f:          
            f.write('\n' + data)   
    else:
        with open(filename, 'w') as f:                   
            f.write(data)
 
def print_time():   
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    data = "Current Time = " + current_time
    return data
 
write_file('test.txt' , print_time())

# Gets DB Credentials and initializes it
cred = credentials.Certificate(
    "vaxxnotifier-firebase-adminsdk-kp0bq-d92a6d817a.json")
# default_app = firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://vaxxnotifier-default-rtdb.firebaseio.com/'
# })

# Get reference to ID of last checked tweet
ref = db.reference('/sinceID')
currSinceIDs = ref.get()
if len(currSinceIDs.values()) > 1:
    raise Exception('Should only have one currSinceID')
for x in currSinceIDs.values():
    currSinceID = x


# currSinceID = "1394273680302149633"
print(currSinceID)

# Variables needed
API_KEY = config('API_KEY')
API_SECRET = config('API_SECRET')
BEARER_TOKEN = config('BEARER_TOKEN')
ACCESS_TOKEN = config('ACCESS_TOKEN')
ACCESS_SECRET = config('ACCESS_SECRET')



# Authorization method


def auth():
    return BEARER_TOKEN

# URL method


def create_url(currSinceID):

    url = f'https://api.twitter.com/2/tweets/search/recent?query=from:1373531468744552448&since_id={currSinceID}&tweet.fields=created_at,in_reply_to_user_id,source,referenced_tweets&max_results=50'
    return(url)

# Headers Method


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
# print(json_response)
# Gets reference to users
usersRef = db.reference('/users')
result = usersRef.get()

# Gets reference to allLocations
locationsRef = db.reference('/locations')
allLocations = locationsRef.get()
locations  = []
for x in allLocations:
    locations.append(allLocations[x])
    
sendOutDict = {}

counter = 0
if 'data' in json_response:
    for x in json_response['data']:
        if counter == 0:
            ref.set({})
            since_id = x['id']
            sinceIDRef = db.reference('/sinceID')
            sinceIDRef.push(since_id)
        counter += 1
        locationsFound = getPotentialAddresses(x['text'],locations)
        print(x['text'].encode('utf'))
        print("")
        for locationFound in locationsFound:
            if locationFound in sendOutDict:
                sendOutDict[locationFound].append(x["text"]+"|||||"+x['id'])
            else:
                sendOutDict[locationFound] = [x['text']+"|||||"+x['id']]



# Loop through list of all users

for person in result:
    # Get and organize user info
    info = result[person].split('|')
    name = info[0]
    location = info[1]
    phonenumber = info[2]
    age = info[3]

    
    for x in sendOutDict.keys():    

        print(x,len(sendOutDict[x]))
        print("------------------")

        if x != location:
            continue


        for i in sendOutDict[x]:
            text = i.split('|||||')[0]
            tweetID = i.split('|||||')[1]
            print("TEXT",text.encode("utf-8"))
            # write_file('test.txt' , "TEXT" + text)
            print("ID",tweetID.encode("utf-8"))
            # write_file('test.txt' , "ID" + tweetID)
            send_alert(name,phonenumber,location,age,text)
        
        
        print("")
        print("")
        




print('end')


write_file('test.txt' , "end")