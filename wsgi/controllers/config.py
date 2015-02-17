#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# Server:
SERVER = 'wsgiref'
# HOST = 'http://smehogar-ekergy.rhcloud.com/'
HOST = 'http://priceprofor-ekergy.rhcloud.com/'

# Meta:
# Note on making it work in localhost:
# * Open a terminal, then do:
#   - sudo gedit /etc/hosts
# * Enter the desired localhost alias for 127.0.0.1:
#   - (e.g. 127.0.0.1 mydomain.tld)
# * Don't forget to save the file :)
# BASE_URI = 'http://smehogar-ekergy.rhcloud.com'
BASE_URI = 'http://priceprofor-ekergy.rhcloud.com'
# Google doesn't seem to accept
# non-working urls, but accepts localhost

# Facebook:
FACEBOOK_CLIENT_ID = '244705875718752'
FACEBOOK_CLIENT_SECRET = '42a6c0c9f1dd726c027f9133e696632a'

# Twitter:
TWITTER_CLIENT_ID = 'RB4h96LxIM7h0UzAOz8iGUvBX'
TWITTER_CLIENT_SECRET = 'GaebMjdmr783zaVqxDmh4H3JtII6hik0YzKcK7aVRC8346S8iv'


"""config.py: Default configuration."""


# import rauth:
import rauth

oauth2 = rauth.OAuth2Service
google_auth = oauth2(
	# get your own app id at google code
    client_id='1080355025565-3hf8s5pves0mvgeo7d80si7litn584g3.apps.googleusercontent.com',
    client_secret='ygotxYVmfNbhkwlwpJJu_BuP',
    name='google',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    base_url='https://accounts.google.com/o/oauth2/auth',
)

google_redirect_uri = '{uri}:{port}/login_success_google'.format(
    uri='http://smehogar-ekergy.rhcloud.com',
    port=80
)

oauth2 = rauth.OAuth2Service
facebook_auth = oauth2(
    client_id=FACEBOOK_CLIENT_ID,
    client_secret=FACEBOOK_CLIENT_SECRET,
    name='facebook',
    authorize_url='https://graph.facebook.com/oauth/authorize',
    access_token_url='https://graph.facebook.com/oauth/access_token',
    base_url='https://graph.facebook.com/'
)
redirect_uri_facebook = '{uri}:{port}/login_success_facebook'.format(
    uri=BASE_URI,
    port=80
)

oauth1 = rauth.OAuth1Service
twitter_auth = oauth1(
    consumer_key=TWITTER_CLIENT_ID,
    consumer_secret=TWITTER_CLIENT_SECRET,
    name='twitter',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
    base_url='https://api.twitter.com/1.1/'
)
request_token, request_token_secret = twitter_auth.get_request_token()
authorize_url_twitter = twitter_auth.get_authorize_url(request_token)
