#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "<ACCESS_TOKEN>"
access_token_secret = "SECRET_ACCESS_TOKEN"
consumer_key = "<CONSUMER_KEY>"
consumer_secret = "CONSUMER_SECRET_KEY"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authentification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    '''
    This line filters Twitter Streams to capture English-language data that's geotagged 
    within the continental United States. 
    ''' 
    stream.filter(locations=[-128.7,25.1,-66.3,49.6], languages=['en'])


