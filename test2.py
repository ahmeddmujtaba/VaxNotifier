from trycourier import Courier
import requests

client = Courier(auth_token="pk_prod_2VV62WNPT1MWJRQQGZM4PFGVH1HX")

url = "https://api.courier.com/profiles/test2" #Change last field to new person

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

#Vaccine Notification
resp = client.send(
  event="8FF168NZCH4N5WH3YYD4QC3QH2KX",
  recipient="test2",
  brand="W79XHG8033MYBEQ7KZ4Y5RGYCEP1",
  profile={
    "phone_number": "16472371699" #change to person's phone #
  },
  data={
    "Firstname": "Jerry Wan", #same as above
    "vaccine_city": "",
    "vaxHunter_post": ""
  }
)

print(resp['messageId'])

#Welcome Notification
resp = client.send(
  event="BVS83ER8B446HHNBRE7BNHT2AT2J",
  recipient="test2",
  profile={
    "phone_number": "16472371699",
  },
  data={
    "firstName": "Jerry",
    "lastName": "Wan",
    "location": "123 sample",
    "age": "18",
  }
)

print(resp['messageId'])

