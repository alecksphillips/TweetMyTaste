TweetMyTaste
============

Like Russian Roulette but with your questionable music taste.

TweetMyTaste randomly tweets whatever you're listening to (via last.fm); better hope it's not one of your guilty pleasures.

Usage
-----
`python TweetMyTaste.py TWITTER_USERNAME LASTFM_USERNAME [-p 'prepended text'] [-a 'appended text'] [-d 'minimum delay'] [-D 'maximum delay']`

User must include their own keys for the Twitter API.
See: https://apps.twitter.com/app/new, and change the CONSUMER_KEY and CONSUMER_SECRET variables to the ones given as "API key" and "API secret" under Application settings. You will have to change the app permissions to allow write access.
