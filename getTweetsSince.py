import requests
import json

import re
from firebase import firebase
from test import send_alert
#cockroach sql --url 'postgres://amujtaba00:jCUTIPzcj-KdOXsV@free-tier5.gcp-europe-west1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&sslrootcert=<your_certs_directory>/cc-ca.crt&options=--cluster=lonely-gecko-289'
firebase = firebase.FirebaseApplication('https://vaxxnotifier-default-rtdb.firebaseio.com/',None)
result = firebase.get('/',None)
print(result)




# Variables needed
API_KEY = 'Sl3MujcYCbOHVXeE2FaGKGYWb'
API_SECRET = 'AMAtoW1hqQJxEe7pbdfNZUZ9V79P3zFTjIOdBl2g3ehHrvDLs3'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAADJzPQEAAAAAnX%2Bwgw3iQR6AvAvxI5ntBfuJ7Eo%3D2yAH66tcNLZ7pvXQvU97qDBl0Q8v90ensr6nbcaCseSsXMGUAv'
ACCESS_TOKEN = '1082426304723648512-vIjzYIinINBOvq3wMT8i5ALs0V0lQN'
ACCESS_SECRET = 'muZyjGgfQwSU5DooluFSnlLfqasD7tQEq9AjBbKbnqCDE'
userID = '1373531468744552448'


# Test Input
province = "[ON]"
city = "Mississauga"
address = "4710 Colombo Crescent"
distance = 15


def auth():
    return BEARER_TOKEN


def create_url():
    url = 'https://api.twitter.com/2/tweets/search/recent?query=from:1373531468744552448&tweet.fields=created_at,in_reply_to_user_id,source&max_results=50'
    return(url)


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


bearer_token = auth()
url = create_url()
headers = create_headers(bearer_token)
json_response = connect_to_endpoint(url, headers)


for person in result:
    info = result[person].split('|')
    name = info[0]
    location = info[1]
    phonenumber = info[2]
    age = info[3]


    for x in json_response['data']:
        try:
            if x['in_reply_to_user_id']:
                continue

        except:
            pass
        if location in x['text']:
            print(x)
            source = x['id']
            tweetURL = f'https://twitter.com/VaxHuntersCan/status/{source}?s=50'
            send_alert(name, phonenumber,location,age,x['text'])
            
print('end')