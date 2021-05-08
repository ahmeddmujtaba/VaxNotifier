import requests
import tweepy

API_KEY = 'Sl3MujcYCbOHVXeE2FaGKGYWb'
API_SECRET = 'AMAtoW1hqQJxEe7pbdfNZUZ9V79P3zFTjIOdBl2g3ehHrvDLs3'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAADJzPQEAAAAAnX%2Bwgw3iQR6AvAvxI5ntBfuJ7Eo%3D2yAH66tcNLZ7pvXQvU97qDBl0Q8v90ensr6nbcaCseSsXMGUAv'
ACCESS_TOKEN = '1082426304723648512-vIjzYIinINBOvq3wMT8i5ALs0V0lQN'
ACCESS_SECRET = 'muZyjGgfQwSU5DooluFSnlLfqasD7tQEq9AjBbKbnqCDE'


userID = '1373531468744552448'

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)


api = tweepy.API(auth)

print(api.me().name)


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if status.text[:2] != "RT":
            print(status.text)
            print(status.created_at)
            print(status.in_reply_to_status_id_str)

            print(" ")


myListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())
myStream.filter(follow=[userID])
