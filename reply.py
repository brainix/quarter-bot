#-----------------------------------------------------------------------------#
#   Quarter Bot - A Twitter bot that flips a coin.                            #
#   reply.py                                                                  #
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
import random

import tweepy

import bot



_EMOJI = [
    u'\U0001F601',
    u'\U0001F602',
    u'\U0001F603',
]



class StreamListener(tweepy.StreamListener):
    def on_data(self, data):
        print('Incoming: {0}'.format(data))
        tweet = json.loads(data)
        screen_name = tweet['user']['screen_name']
        me = screen_name == bot.SCREEN_NAME
        retweet = 'retweeted_status' in tweet
        if not me and not retweet:
            side = random.choice(bot.SIDES)
            hashtag = random.choice(bot.HASHTAGS)
            emoji = random.choice(_EMOJI)

            # I swear that the next line of code isn't Ruby.
            reply = u'@{0} {1}. #{2} {3}'.format(screen_name, side, hashtag, emoji)
            try:
                log = u'Outgoing: {0}'.format(reply)
                print(log)
            except UnicodeEncodeError:
                log = bot.unicode_to_ascii(reply)
                log = u'Outgoing: {0}'.format(log)
                print(log)

            if bot.ENV == 'production':
                try:
                    bot.api.update_status(reply, tweet['id'])
                except tweepy.TweepError:
                    pass

        # Return True to keep the stream listener listening.
        return True



def main():
    listener = StreamListener()
    stream = tweepy.Stream(bot.auth, listener)
    stream.filter(track=bot.PHRASES)

if __name__ == '__main__':
    main()
