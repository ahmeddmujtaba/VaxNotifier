# from firebase import firebase
from trycourier import Courier
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from twilio.rest import Client
import decouple
from decouple import config

# Gets DB Credentials and initializes it
cred = credentials.Certificate(
    "vaxxnotifier-firebase-adminsdk-kp0bq-d92a6d817a.json")
cred = credentials.Certificate(config('FB_CRED'))
# default_app = firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://vaxxnotifier-default-rtdb.firebaseio.com/'
# })
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': config('FB_URL')
})
# firebase = firebase.FirebaseApplication('https://vaxxnotifier-default-rtdb.firebaseio.com/',None)


account_sid = config('TWILIO_SID')
auth_token = config('TWILIO_AUTH_TOKEN')

client = Client(account_sid,auth_token)
phonenumber = '+17053000629'
phonenumber = config('PHONE_NUMBER')

# THIS IS ONLY FOR INITIAL SIGN UP
def send_message(name, tophone_number,location,age):

    text = f''' Hi {name}, you will recieve notifications from VaxNotifier. Details: 
    Location : {location}
    PhoneNumber: {tophone_number}
    Age: {age}
    '''

    message = client.messages.create(body=text,to=tophone_number,from_=phonenumber)

    # Add to firebase as well
    new_user = f'{name}|{location}|{tophone_number}|{age}'
    ref = db.reference('/users')
    ref.push(new_user)

    locationRef = db.reference('/locations')
    allLocations = locationRef.get()
    found = False
    if allLocations == None:
        locationRef.push(location)
    else:
        for x in allLocations:
            
            if location == allLocations[x]:
                found = True
        if not found:
            locationRef.push(location)



 

 


def send_alert(name,tophone_number,location,age,tweet):
    text = f''' Hi {name}, we have found vaccine availability in {location}. Details: 
    {tweet}
    '''
    message = client.messages.create(body=text,to=tophone_number,from_=phonenumber)

    print(message.sid)



