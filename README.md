# @scihubot

## About the repo

This repo implements @scihubot, a twitterbot that serves as an interface between users and a sci-hub server. It monitors Twitter mentions, processes the messages and replies to them with a download url for the papers. The code runs remotely on Heroku, for the time being.         
    
## Example
    
Say that you've come across a super interesting paper, but bad luck, it's behind a paywall -- no worries, just tweet @scihubot. Tweets must have this structure:        
`@scihubot _your_DOI_` or `@scihubot _paper_url_`      
The bot will reply prompty with a download link (`#file.io/abc123`), which you will have to copy+paste into your browser to start the downloads. The links are valid for one download.      
Support for books, which requires libgen access, is available, although in trial. So for the moment, the bot supports access to papers and books through DOI and direct urls.      

## Contributing

Feel free to fork the repo to contribute to it, or clone it if you want to deploy your own bot. The more the merrier - however, you should be aware of the possible implications of running the code and associating with sci-hub, and my discharge of responsibilities regarding them (read the licence).              

## Acknowledgments

* twitter users for trying out the bot, and helping me find bugs
* [stackoverflow](https://stackoverflow.com/)
