#-----------------------------------------------------------------------------#
#   Quarter Bot - A Twitter bot that flips a coin.                            #
#   bot.py                                                                    #
#                                                                             #
#   Copyright (c) 2014, Seventy Four, Inc.                                    #
#                                                                             #
#   This program is free software: you can redistribute it and/or modify      #
#   it under the terms of the GNU General Public License as published by      #
#   the Free Software Foundation, either version 3 of the License, or         #
#   (at your option) any later version.                                       #
#                                                                             #
#   This program is distributed in the hope that it will be useful,           #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#   GNU General Public License for more details.                              #
#                                                                             #
#   You should have received a copy of the GNU General Public License         #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.     #
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
            try:
                api.update_status(response, tweet['id'])
            except tweepy.TweepError:
                pass
        return True



def main():
    listener = StreamListener()
    stream = tweepy.Stream(auth, listener)
    stream.filter(track=PHRASES)

if __name__ == '__main__':
    main()
