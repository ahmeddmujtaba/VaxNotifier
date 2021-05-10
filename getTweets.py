import requests
import tweepy



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
