#-----------------------------------------------------------------------------#
#   bot.py                                                                    #
#                                                                             #
#   Copyright (c) 2014, Seventy Four, Inc.                                    #
#   All rights reserved.                                                      #
#-----------------------------------------------------------------------------#



import json
import os
import random

import tweepy



PHRASES = ['coin flip', 'coin toss', '#FlipACoin']
RESPONSES = ['Heads', 'Tails']

SCREEN_NAME = os.environ['TWITTER_SCREEN_NAME']
CONSUMER_KEY = os.environ['TWITTER_API_KEY']
CONSUMER_SECRET = os.environ['TWITTER_API_SECRET']
ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']



auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)



class StreamListener(tweepy.StreamListener):
    def on_data(self, data):
        print(data)
        tweet = json.loads(data)
        screen_name = tweet['user']['screen_name']
        me = screen_name == SCREEN_NAME
        retweet = 'retweeted_status' in tweet
        if not me and not retweet:
            response = random.choice(RESPONSES)
            response = '@{0} {1}. #FlipACoin'.format(screen_name, response)
            api.update_status(response, tweet['id'])
        return True



def main():
    listener = StreamListener()
    stream = tweepy.Stream(auth, listener)
    stream.filter(track=PHRASES)

if __name__ == '__main__':
    main()
