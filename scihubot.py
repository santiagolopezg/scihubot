'''
scihubot.py
'''

import urllib.request as urllib2
import requests
import time
import json
import subprocess
from subprocess import check_output
import os
import tweepy
from tweepy import Stream

CONSUMER_KEY = 'consumer_key'
CONSUMER_SECRET = 'consumer_secret'
ACCESS_KEY = 'access_key'
ACCESS_SECRET = 'access_secret'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
twitterApi = tweepy.API(auth)

try:
    twitterApi.verify_credentials()
    print("Authentication OK")
    print ('bot v3.6')
except:
    print("Error during authentication")

url = 'https://sci-hub.tw/'
account_screen_name = 'username'
account_user_id = 'user_id'

def navigate_web(url, user_input):
    # takes a paper's DOI or URL and downloads pdf locally. Also returns DOI
	# say, the DOI is 10.1126/science.aao5167, or the URL is http://science.sciencemag.org/content/359/6373/343/tab-pdf

    size = 0
    while size < 1820: # sometimes, a limit is reached and a captcha has to be filled in -
						# in that case, the file generated will be damaged and about 1820
        query = url+user_input
        html = urllib2.urlopen(query).read().decode("utf-8")

        ## if it's a book, not a paper:
        if 'libgen' in html:
            # <a href="http://80.82.78.13/get.php?md5=4309eeedc2264d5dad4fa1e5f04d5d8c&amp;key=1A6PK2X6FM7069HK&amp;mirr=1"><h2>GET</h2></a>
            p = html.split('title="Gen.lib.rus.ec">Gen.lib.rus.ec</a></td><td width="10%" align="center"><a href="')[1].split('" title="Libgen.lc">')[0]
            doi = p.split('=')[1]
            html = urllib2.urlopen(p).read().decode("utf-8")
            q= html.split('valign="top" bgcolor="#A9F5BC"><a href="')[1].split('"><h2>GET</h2>')[0]

        ## it's a paper:
        else:
            q = html[html.find('"location.href=')+len('"location.href=')+1:html.find('.pdf')+4]
            print (q, 'query')
            doi = q.split('.pdf')[0]
            doi = doi.split('/')
            doi = doi[len(doi)-1]

		## if the bot can't find the paper:
        if len(q) == 0:
            return 0, 0

		## if it found the paper, the link, but somehow the http is missing:
        if 'https' not in q:
            q = 'https:' + q

        ### download the document ###
        r = requests.get(q)
        time.sleep(10) ## I realised that sometimes the requests weren't fetched correctly, and the PDF files
                        ## ended up damaged. Adding a sleeping period seems to help in guaranteeing file integrity
        print ("writing file...")
        with open('{0}.pdf'.format(doi), 'wb') as f:
            f.write(r.content)

        size = os.stat('{0}.pdf'.format(doi)).st_size
        if size < 1820: # give the server time to overcome the limit and stop requesting the captcha
            time.sleep(60)
	## now I have the file locally, I should store it on expirebox.com and have it give me a download link
    comm = 'curl -F file=@{0} https://file.io/?expires=1w'.format(doi+'.pdf')
    output = check_output(comm.split())
    output = json.loads(output.decode('utf-8'))
    key = output["key"]
    return doi, key

class ReplyToTweet(tweepy.StreamListener):
    def on_data(self, data):
        tweet = json.loads(data.strip())
        retweeted = tweet.get('retweeted')
        from_self = tweet.get('user',{}).get('id_str','') == account_user_id

        if retweeted is not None and not retweeted and not from_self:
            ## Now, I have the user who tweeted to me, and the DOI / link to be processed

            tweetId = tweet.get('id_str')
            screenName = tweet.get('user',{}).get('screen_name')
            tweetText = tweet.get('text')
            tweetText = tweetText.split(' ')
            tweetText = tweetText[len(tweetText)-1]

            if 'https' in tweetText: # e.g. https://t.co/xQwRV8tQwk
                session = requests.Session()
                resp = session.head(tweetText, allow_redirects=True)
                resp = session.head(resp.url, allow_redirects=True)
                tweetText = resp.url

            else:
                tweetText = tweetText.strip('DOI:')
                tweetText = tweetText.strip('doi:')
                tweetText = tweetText.strip('Doi:')

            if 'http' in tweetText or 'doi' not in tweetText and '.' in tweetText and '/' in tweetText:

            	## it has DOI or link in it
                try:
                    paper, link = navigate_web(url, tweetText)
                    if (paper, link) == (0, 0):
                        replyText = 'Hi @' + screenName + ", I'm sorry I couldn't find the paper - maybe try again later?"

                    else:
                        replyText = 'Hi @' + screenName + ', here you go - ' + '#https://file.io/'+ link + ' (copy+paste link w/o #)'
                        #replyText = 'Hi @' + screenName + ', here you go - #'+ link + ' (copy+paste link w/o #)'


                    print('Tweet ID: ' + tweetId)
                    print('From: ' + screenName)
                    print('Tweet Text: ' + tweetText)
                    print('Reply Text: ' + replyText)

                    twitterApi.update_status(status=replyText, in_reply_to_status_id=tweetId)
                    print ('removing paper from local dir...')
                    os.remove('{0}.pdf'.format(paper))
                except:
                    pass

    def on_error(self, status):
        time.sleep(20)

### Test part ###

## papers
#a = navigate_web('https://sci-hub.tw/', '10.1111/aogs.13013') #works
#a = navigate_web('https://sci-hub.tw/', '10.1126/science.aao5167') #works
#a = navigate_web('https://sci-hub.tw/', '10.1111/j.1467-971X.1995.tb00340.x') #works
#a = navigate_web('https://sci-hub.tw/', '10.1111/j.1467-971X.1987.tb00185.x') #works
#a = navigate_web('https://sci-hub.tw/', '10.1007/978-94-017-0910-1') # works
#a = navigate_web('https://sci-hub.tw/', 'https://doi.org/10.1038/s41591-020-0844-1') #works!


## books
#a = navigate_web('https://sci-hub.tw/', '10.1002/bmb.2005.494033010419')
#a = navigate_web('https://sci-hub.tw/', '10.1002/bmb.20192')
#a = navigate_web('https://sci-hub.tw/', '10.1002/mrd.1120170110')
#a = navigate_web('https://sci-hub.tw/', '10.1007/978-3-319-60928-7_18')
#a = navigate_web('https://sci-hub.tw/', '10.1007/978-1-4614-7138-7')


while True:
    streamListener = ReplyToTweet()
    twitterStream = Stream(auth = auth, listener = streamListener)
    twitterStream.filter(follow=[account_user_id]) # user ID for scihubot account
