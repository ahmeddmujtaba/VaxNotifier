from firebase import firebase
from trycourier import Courier
import requests

firebase = firebase.FirebaseApplication('https://vaxxnotifier-default-rtdb.firebaseio.com/',None)


# THIS IS ONLY FOR INITIAL SIGN UP
def send_message(name, phone_number,location,age):

    client = Courier(auth_token="pk_prod_2VV62WNPT1MWJRQQGZM4PFGVH1HX")

    url = "https://api.courier.com/profiles/" + \
        name  # Change last field to new person

    payload = {"profile": {
        "name": "Jerry Wan",
        "phone_number": "16472371699"
    }
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer pk_prod_2VV62WNPT1MWJRQQGZM4PFGVH1HX"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)

    # Add to firebase as well
    new_user = f'{name}|{location}|{phone_number}|{age}'
    result = firebase.post('/', new_user, params={'print': 'pretty'})
    print(result)

    resp = client.send(
  event="BVS83ER8B446HHNBRE7BNHT2AT2J",
  recipient="test2",
  profile={
    "phone_number": phone_number,
  },
  data={
    "firstName": name,
    "lastName": "",
    "location": location,
    "age": age,
  }
)

    print(resp['messageId'])


def send_alert(name,phone_number,location,age,tweet):
    client = Courier(auth_token="pk_prod_2VV62WNPT1MWJRQQGZM4PFGVH1HX")

    url = "https://api.courier.com/profiles/" + \
        name  # Change last field to new person

    payload = {"profile": {
        "name": "Jerry Wan",
        "phone_number": "16472371699"
    }
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer pk_prod_2VV62WNPT1MWJRQQGZM4PFGVH1HX"
    }

    response = requests.request("POST", url, json=payload, headers=headers)


    resp = client.send(
        event="8FF168NZCH4N5WH3YYD4QC3QH2KX",
        recipient="test2",
        brand="W79XHG8033MYBEQ7KZ4Y5RGYCEP1",
        profile={
            "phone_number": phone_number  # change to person's phone #
        },
        data={
            "Firstname": name,  # same as above
            "vaccine_city": location,
            "vaxHunter_post": tweet
        }
    )

    print(resp['messageId'])