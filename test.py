import csv
from csv import writer
from trycourier import Courier
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from twilio.rest import Client
import decouple
from decouple import config
from twilio.twiml.messaging_response import MessagingResponse


# Gets DB Credentials and initializes it
#cred = credentials.Certificate(
#    "vaxxnotifier-firebase-adminsdk-kp0bq-d92a6d817a.json")
#cred = credentials.Certificate(config('FB_CRED'))
# default_app = firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://vaxxnotifier-default-rtdb.firebaseio.com/'
# })
#default_app = firebase_admin.initialize_app(cred, {
#    'databaseURL': config('FB_URL')
#})
# firebase = firebase.FirebaseApplication('https://vaxxnotifier-default-rtdb.firebaseio.com/',None)


account_sid = config('TWILIO_SID')
auth_token = config('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)
phonenumber = '+17053000629'
phonenumber = config('PHONE_NUMBER')

# THIS IS ONLY FOR INITIAL SIGN UP


def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    resp.message("The Robots are coming! Head for the hills!")

    return str(resp)


def send_message(name, tophone_number, location, age):

    text = f''' Hi {name}, you will recieve notifications from VaxNotifier. Details: 
    Location : {location}
    PhoneNumber: {tophone_number}
    Age: {age}
    '''

    message = client.messages.create(
        body=text, to=tophone_number, from_=phonenumber)

    # Add to firebase as well
    new_user = f'{name}|{location}|{tophone_number}|{age}'
    writeCSV("users.csv", new_user)

    allLocations = readCSVList("locations.csv")
    found = False
    if allLocations == None:
        writeCSV("locations.csv", location)
    else:
        for x, i in enumerate(allLocations):
            print(allLocations[x])

            if location == allLocations[x]:
                found = True
        if not found:
            writeCSV("locations.csv", location)


def send_alert(name, tophone_number, location, age, tweet):
    text = f''' Hi {name}, we have found vaccine availability in {location}. Details: 
    {tweet}
    '''
    message = client.messages.create(
        body=text, to=tophone_number, from_=phonenumber)

    print(message.sid)


def writeCSV(filename, data):
    with open(filename, 'a') as f_object:

        # Pass this file object to csv.writer()
        # and get a writer object
        writer_object = writer(f_object)

        # Pass the list as an argument into
        # the writerow()
        writer_object.writerow([data])

        # Close the file object
        f_object.close()


def emptyCSV(filename):
    with open(filename, 'w') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow([])
        f_object.close()


def readCSVList(filename):
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            try:
                data.append(row[0].replace('"', ''))
            except:
                continue
        return data


# send_message("Ahmed Mujtaba", "16477464125", "Milton", "20")
