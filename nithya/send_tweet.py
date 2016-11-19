import twitter_cred as cred
try:
    import json
except ImportError:
    import simplejson as json

from twitter import *
# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Variables that contains the user credentials to access Twitter API

def create_tweet(new_status):
    oauth = OAuth(cred.user_info['ACCESS_TOKEN'], cred.user_info['ACCESS_SECRET'], cred.user_info['CONSUMER_KEY'],
                  cred.user_info['CONSUMER_SECRET'])

    # Initiate the connection to Twitter Streaming API
    twitter_stream = TwitterStream(auth=oauth)

    twitter = Twitter(auth=oauth)
    #new_status = 'Mandatory Hackathon Post'
    results = twitter.statuses.update(status = new_status)

if __name__ == '__main__':
    create_tweet('Mandatory Hackathon Post')
