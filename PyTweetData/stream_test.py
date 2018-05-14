import tweepy
from tweepy import OAuthHandler
from cfg import APP_Config

from tweepy import Stream
from tweepy.streaming import StreamListener


class MyListener(StreamListener):
    def on_data(self,data):
        try:
            with open('Blockchain.json','a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print('Error on_data:%s' % str(e))
        return True

    def on_error(self,status):
        print(status)
        return True

auth = OAuthHandler(APP_Config['USER_KEY'],APP_Config['USER_SECRET'])
auth.set_access_token(APP_Config['ACCESS_TOKEN'],APP_Config['ACCESS_SECRET'])

twi_stream = Stream(auth, MyListener())
twi_stream.filter(track=['#BlockChain','#Blockchain','#blockchain'])