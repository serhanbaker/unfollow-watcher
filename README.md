#UnfollowWatcher

### Installation and Running

1. Clone this repo
2. To install dependencies, enter `pip install -r requirements.txt` 
3. Create a twitter app from https://dev.twitter.com/apps
4. Open twitter_settings.py.example, enter your credentials. You can also edit Redis settings
5. You can configure the time interval, too (I would recommend making it not less than 60 seconds).
6. Go `python watcher.py` and it will check for your unfollowers every X seconds (where X is defined time interval in seconds)
7. This must be running at all time in order to track unfollowers continuously. You can terminate it by pressing Ctrl + C while running 

## How Does it Work?

It's pretty simple actually. Gets twitter followers, loads them into Redis with SADD command, then loads again with a different set after a while, 
and finally gets difference with something like `SDIFF followers followers_new`. Then deletes both sets and repeats the process
The diff won't contain new followers, because it only gets the items that have in A, but not B

### Author
[Serhan Baker](http://serhanbaker.com)
