'''
scihubot.py
'''

import urllib2
import requests
import random
import datetime
import json
import ConfigParser
import subprocess
import os

import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream


CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
twitterApi = tweepy.API(auth)

url = 'http://sci-hub.tw/'

account_screen_name = 'scihubot'
account_user_id = ''


class ReplyToTweet(StreamListener):

    def on_data(self, data):
        print data
        tweet = json.loads(data.strip())
        
        retweeted = tweet.get('retweeted')
        from_self = tweet.get('user',{}).get('id_str','') == account_user_id

        if retweeted is not None and not retweeted and not from_self:
            ## Now, I have the user who tweeted to me, and the DOI / link to be processed

            tweetId = tweet.get('id_str')
            screenName = tweet.get('user',{}).get('screen_name')
            tweetText = tweet.get('text')
            print tweetText
            
            tweetText = tweetText.split(' ')[1]
                        
            
            if 'http' not in tweetText:
            	## it has DOI or link in it
            	try:
					paper, link = navigate_web(url, tweetText)
		   
					replyText = 'Hi @' + screenName + ', here you go! ' + '#https://file.io/'+ link + ' (copy+paste link w/o #)'
					
					print('Tweet ID: ' + tweetId)
					print('From: ' + screenName)
					print('Tweet Text: ' + tweetText)
					print('Reply Text: ' + replyText)
					
					twitterApi.update_status(status=replyText, in_reply_to_status_id=tweetId)
					print 'removing paper from local dir...'
					os.remove('{0}.pdf'.format(paper))
					
            	except:
					pass
			
    def on_error(self, status):
        print status, 'shit'

def navigate_web(url, user_input):
	# takes a paper's DOI and downloads pdf locally. Also returns DOI
	# say, the DOI is 10.1126/science.aao5167, or the URL is http://science.sciencemag.org/content/359/6373/343/tab-pdf
	
	query = url+user_input
	html = urllib2.urlopen(query).read()
	
	print 'begin html:'
	
	q = html[html.find('<iframe src = "')+15:html.find('.pdf')+4]
	
	if 'http' not in q:
		q = 'http:' + q
		
	doi = q.split('.pdf')[0]
	doi = doi.split('/')
	doi = doi[len(doi)-1]
	print doi 
	
	
	r = requests.get(q)
	
	with open('{0}.pdf'.format(doi), 'wb') as f:
		f.write(r.content)
	
	comm = 'curl -F file=@{0} https://file.io/?expires=1w'.format(doi+'.pdf')

	process = subprocess.Popen(comm.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()

	link = output.split('"key":')[1][1:7]
	
	return doi, link

while True:
    streamListener = ReplyToTweet()
    twitterStream = Stream(auth, streamListener)
    twitterStream.userstream(_with='user')
