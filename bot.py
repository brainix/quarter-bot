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



import os
import unicodedata

import tweepy



ENV = os.environ['ENV']
SCREEN_NAME = os.environ['TWITTER_SCREEN_NAME']
CONSUMER_KEY = os.environ['TWITTER_API_KEY']
CONSUMER_SECRET = os.environ['TWITTER_API_SECRET']
ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

PHRASES = ['coin flip', 'coin toss', 'heads tails', '#FlipACoin', '#HeadsOrTails']
SIDES = ['Heads', 'Tails']
HASHTAGS = ['FlipACoin', 'HeadsOrTails']



auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)



def unicode_to_ascii(s):
    # lol
    s = unicodedata.normalize('NFKD', s)
    s = s.encode('ascii', 'ignore')
    s = s.strip()
    return s

def get_items(*args, **kwargs):
    cursor = tweepy.Cursor(*args, **kwargs)
    pages = cursor.pages()
    items = []
    for page in pages:
        items.extend(page)
    items = set(items)
    return items
