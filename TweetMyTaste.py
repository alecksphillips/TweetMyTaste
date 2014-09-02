#!/usr/bin/env python
#
# TweetMyTaste.py - Like Russian Roulette but with your questionable music
# taste.
#
# Copyright (C) 2014  Alex Phillips
#

#########################
# GPL Information
#########################
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# See <http://www.gnu.org/licenses/> for more information
#
#########################

try:
    from urllib.request import urlopen
    import urllib.error
except ImportError:
    from urllib2 import urlopen
    import urllib2.error
from xml.dom import minidom
import sys
import os.path
import time
import random
import argparse
from twitter import *

description = 'TweetMyTaste.py - like Russian Roulette but with your questionable music taste'

#You can change this
lastfm_api_key='6a89f951803d3af3d65abc47e9cbfebb'

#You must include your own keys here (see: https://apps.twitter.com/app/new)
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

local_copy = 'nowplaying.xml'

#Putting defaults at top of file for reference
defaults = dict()
defaults['prepend'] = 'Now playing: '
defaults['append'] = ''
defaults['min_delay'] = 1800
defaults['max_delay'] = 14400

args = dict()

def main():
    get_parameters()
    
    #Storing oauth tokens locally
    TWITTER_CREDS = args['twitter_username'] + '_creds.txt'
    
    if not os.path.exists(TWITTER_CREDS):
        oauth_dance("TweetMyTaste", CONSUMER_KEY, CONSUMER_SECRET, TWITTER_CREDS)
        
    oauth_token, oauth_secret = read_token_file(TWITTER_CREDS)
    
    twitter = Twitter(auth=OAuth(
    oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))
    
    print('Starting with arguments:')
    print('Twitter Username: ' + args['twitter_username'])
    print('Last.fm Username: ' + args['lastfm_username'])
    print('Prepended text: ' + args['prepend'])
    print('Appended text: ' + args['append'])
    print('Minimum delay: ' + str(args['min_delay']))
    print('Maximum delay: ' + str(args['max_delay']))
    
    #Keeping track of the last track that was playing using track url
    last_track = ''
    
    feed_url = ('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user='
    + args['lastfm_username'] + '&api_key=' + lastfm_api_key + '&limit=1')
    
    while True:
        #Wait a random time before doing a tweet
        time.sleep(random.randrange(args['min_delay'], args['max_delay']))
        
        download(feed_url,local_copy)
        
        data=open(local_copy,'rb')
        xmldoc=minidom.parse(data)
        data.close()
        
        item = xmldoc.getElementsByTagName('track')[0]
        
        #If track playing
        if (item.attributes.item(0)):
        
            current_track = item.getElementsByTagName('url')[0].firstChild.data
            
            #If track changed
            if (current_track != last_track):
            
                last_track = current_track
                artist = item.getElementsByTagName('artist')[0].firstChild.data
                track = item.getElementsByTagName('name')[0].firstChild.data
                
                track_data= args['prepend'] + artist + ' - ' + track + args['append']
                
                #Tweet it
                twitter.statuses.update(status=track_data)
                
        #Else, nothing playing
        else:
            #If only just stopped playing
            if(last_track != ''):
                
                last_track = ''
                track_data = ''
            
#Get command line arguments
def get_parameters():
    parser = argparse.ArgumentParser(prog='TweetMyTaste.py',description=description)
    parser.add_argument('twitter_username')
    parser.add_argument('lastfm_username')
    parser.add_argument('-p', '--prepend', dest = 'prepend', default = defaults['prepend'])
    parser.add_argument('-a', '--append', dest = 'append', default = defaults['append'])
    parser.add_argument('-d', '--min_delay', dest = 'min_delay', default = defaults['min_delay'], type=int)
    parser.add_argument('-D', '--max_delay', dest = 'max_delay', default = defaults['max_delay'], type=int)
    
    input = parser.parse_args()
        
    args['twitter_username'] = input.twitter_username
    args['lastfm_username'] = input.lastfm_username
    args['prepend'] = input.prepend
    args['append'] = input.append
    if input.min_delay < 1:
        print('#'*20)
        print('Delay must be AT LEAST 1 second, setting to 1 second')
        print('#'*20)
        args['min_delay'] = 1
    else:
        args['min_delay'] = input.min_delay
    
    if input.max_delay < args['min_delay']:
        print('#'*20)
        print('Max delay must be greater than or equal to min delay, setting to be equal to min delay')
        print('#'*20)
        args['max_delay'] = args['min_delay']
    else:
        args['max_delay'] = input.max_delay
        

#Download xml as binary
def download(url,filename):
    try:
        instream=urlopen(url)
        outfile=open(filename,'wb')
        for chunk in instream:
            outfile.write(chunk)
        instream.close()
        outfile.close()
    except Exception as e:
        print(e)
        sys.exit()

if __name__=="__main__":
    main()
