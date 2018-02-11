# @scihubot

## About the repo

This repo allows for the implementation of a Twitter bot (mine is @scihubot), which serves as an interface between users and a sci-hub server. It monitors Twitter mentions, processes the messages and replies to them with a download url for the papers. The code runs in a virtualenv on Heroku, for the time being.         
I realised that access to sci-hub is usually user-limited, rather than server-limited. Hence, cloud-basing the request-response system (here, Heroku) might help to bypass numerous headaches and facilitate access to paywalled papers.            
Despite the recent push for open science, prestigious journals still maintain a monopoly on what they consider to be high-impact papers, and the publishing of the aforementioned. This often means that it is prohibitively expensive to access them (ironically, [reported in Science](http://www.sciencemag.org/news/2016/04/whos-downloading-pirated-papers-everyone)). Until this is amended, initiatives such as sci-hub, libgen and the derived software implementations (e.g. [auto-scihub bookmark](https://github.com/nfahlgren/scihub_bookmark)) for bypassed access will continue to proliferate. 

## Getting Started

This script runs on Python 2.7.14 (see the `runtime.txt` file). I haven't tested it on 3.x, but since it will ultimately be run on a dyno, this doesn't matter much if you'll be pushing the app as it stands.        
Before you clone the repo, and considering that you eventually want to deploy on Twitter, you'll need to create an account, an associated Twitter app, etc. - you can read about it [here](http://briancaffey.github.io/2016/04/05/twitter-bot-tutorial.html). The bot will use a particular feature of the Tweepy package, called Streaming. You can read about it [here](http://docs.tweepy.org/en/v3.5.0/streaming_how_to.html). Also sign up for a [Heroku account](https://signup.heroku.com), if you'd like to keep the bot up and running.       

## Installing

Once this is done, start by cloning/forking the repo (i.e.: `git clone https://github.com/santiagolopezg/scihubot`). Then, make sure you have the dependencies installed. They include:      
```     
urllib2      
requests        
random      
datetime        
json        
ConfigParser       
subprocess         
tweepy           
pipenv
```     
Note that most of these will be included in your python installation (I use Anaconda), but you can double-check anyways.    
        
Once you have created your Twitter account and obtained the authentification keys and such, go ahead and edit the `scihubot.py` file:     
```
CONSUMER_KEY = '_your_consumer_key_'
CONSUMER_SECRET = '_your_secret_'
ACCESS_KEY = '_your_access_key_'
ACCESS_SECRET = '_your_access_secret_'

...

account_screen_name = '_your_account_screename_' ## i.e. mine is scihubot
account_user_id = '_your_user_ID_' ## Usually a long number, i.e. 0123456789

```
      
Once this is done, you can essentially start running the code from cmd line, i.e.: `python scihubot.py`. The issue is that the bot will crash (actually, stop listening to Twitter) when you terminate the session. That is why I recommend that you deploy on Heroku, or a other similar platform.     
If you decide to use Heroku, now is a good time to log in (`heroku login` - enter your creds),  create your app (`heroku create`) then add your code (`git add .`), commit it (`git commit -m 'my first commit'`) and push it (`git push heroku master`) to your remote git repo (on heroku). Once this is done, you can make sure that an instance of the app is running (`heroku ps:scale web=1`).    
Once you have the app running, you can remotely check the logs (`heroku logs --ps worker`), or `heroku logs --tail` if you want to keep streaming the logs. They are also available from your heroku dashboard. You can read more about heroku and python [here](https://devcenter.heroku.com/articles/getting-started-with-python#introduction).  

## Example

Say that you've come across a super interesting paper, but oh bad luck, it's behind a paywall! No worries, just tweet at your friendly bot.     
For the time being, tweets must have this structure:     
`@scihubot _your_DOI_` or `@scihubot _your_papers_url_`      
The bot will reply prompty, with a hashed [file.io](https://www.file.io/#one) link (i.e. `#file.io/abc123`), which you will have to copy+paste into your browser to start the downloads. For the sake of swiftness, the links expire as soon as they're used. I'm sure that if you want a re-usable link, you could find another file-hosting domain.      
Support for books, which requires libgen access, is available, although in trial. So for the moment, the bot supports access to papers and books through DOI and direct urls. 

## Deployment

As mentioned previously, I've deployed the app on Heroku, but there are plenty of alternatives for hosting your project. 

## To do

* Test support for libgen (i.e. books);        
* Implement independent local and remote module tests      
* Other stuff I'm forgetting / discovering

## Built With

* [Tweepy](http://www.tweepy.org/)
* [Heroku](heroku.com)

## Contributing

Feel free to fork the repo to contribute to it, or clone it if you want to deploy your own sci-hub bot. The more the merrier!     

## Acknowledgments

* Random twitter users for trying out the bot, and helping me find bugs
* [stackoverflow](https://stackoverflow.com/)
