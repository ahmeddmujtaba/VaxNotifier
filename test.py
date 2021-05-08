'''
from trycourier import Courier

client = Courier(auth_token="pk_prod_2VV62WNPT1MWJRQQGZM4PFGVH1HX")
resp = client.send(
    event="courier-quickstart",
    recipient="Google_116554302925116678380",
    data={
      "favoriteAdjective": "awesomeness"
    }
)

print(resp['messageId'])
'''

from trycourier import Courier
import requests


def send_message(name, phone_number,location):

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

    resp = client.send(
        event="8FF168NZCH4N5WH3YYD4QC3QH2KX",
        recipient="test2",
        brand="W79XHG8033MYBEQ7KZ4Y5RGYCEP1",
        profile={
            "phone_number": phone_number  # change to person's phone #
        },
        data={
            "Firstname": name,  # same as above
            "vaccine_address": "",
            "vaccine_city": "",
            "VaxHunter_link": ""
        }
    )

    print(resp['messageId'])
