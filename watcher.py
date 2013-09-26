#!/usr/bin/python
import time
import tweepy
import twitter_settings
from sys import exit

class TwitterStats():
  def initialize_app(self):
    interval_secs = twitter_settings.interval_secs
    app_key = twitter_settings.consumer_key
    app_secret = twitter_settings.consumer_secret
    oauth_token = twitter_settings.oauth_token
    oauth_token_secret = twitter_settings.oauth_token_secret

    oauth = tweepy.OAuthHandler(app_key, app_secret)
    oauth.set_access_token(oauth_token, oauth_token_secret)

    twitter_gate = tweepy.API(oauth)
    user = twitter_gate.me()

    print ("Hey, %s, you have %d followers!" % (user.screen_name, user.followers_count))
    print ("I will check every %s seconds and alert you when someone unfollows you" % (interval_secs))

    init_followers_set = self.get_followers(twitter_gate)
    marked = set()

    while True:
      time.sleep(interval_secs)
      curr_followers_set = self.get_followers(twitter_gate)
      unfollowers_set = set()    
      if curr_followers_set:
        unfollowers_set = init_followers_set - curr_followers_set - marked
        init_followers_set = curr_followers_set
      for tw_id in unfollowers_set:
        try:
          unfollower = self.get_marked(twitter_gate, tw_id)
          marked.add(tw_id)
          print ("@%s (%s) has just unfollowed you!" % (unfollower.screen_name, unfollower.name))
        except Exception, e:
          raise e
      if marked:
        print ("You have %d followers now" % (len(init_followers_set)))

  def get_followers(self, twitter_gate):
    try:
      return set(tweepy.Cursor(twitter_gate.followers_ids).items())
    except Exception as e:
      raise e

  def get_marked(self, twitter_gate, tw_id):
    try:
      return twitter_gate.get_user(tw_id)
    except Exception, e:
      raise e
  

def main():
  twitter_stats = TwitterStats()
  twitter_stats.initialize_app()

if __name__ == '__main__':
  main()
