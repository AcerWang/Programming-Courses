import tweepy
from tweepy import OAuthHandler
from cfg import APP_Config
import json
# In order to authorise our app to access Twitter on our behalf,
# we need to use the OAuth interface:
auth = OAuthHandler(APP_Config['USER_KEY'],APP_Config['USER_SECRET'])
auth.set_access_token(APP_Config['ACCESS_TOKEN'],APP_Config['ACCESS_SECRET'])

# The API class provides a wrapper for the API as provided by Twitter
# You can use the API to get more detail information of your account. 
api = tweepy.API(auth)

# Use this to test the authorization is ok.
# It should print your twitter account name. 
print(api.me().name)

# Get all of the authorized user timeline data.
# we output the tweets created time and text.
for tweet in tweepy.Cursor(api.user_timeline).items():
    #print(tweet._json['created_at']+" : "+tweet._json['text'])
    print(json.dumps(tweet._json,indent=4))


print('-------------------------------------------------------------------------------')

# Get friends info we follows on twitter
# print friend id, screen name, and location for each.
# for friend in tweepy.Cursor(api.friends).items(10):
#      print(friend._json['id'],": "+friend._json['screen_name']+" @ "+friend._json['location'])