#!/usr/bin/python
import time
import tweepy
import twitter_settings
import redis

def main():
  interval_secs = twitter_settings.interval_secs
  app_key = twitter_settings.consumer_key
  app_secret = twitter_settings.consumer_secret
  oauth_token = twitter_settings.oauth_token
  oauth_token_secret = twitter_settings.oauth_token_secret
  host = twitter_settings.host
  port = twitter_settings.port
  db = twitter_settings.db
  r = redis.StrictRedis(host, port, db)
  r.delete('followers', 'followers_new')

  oauth = tweepy.OAuthHandler(app_key, app_secret)
  oauth.set_access_token(oauth_token, oauth_token_secret)

  api = tweepy.API(oauth)
  user = api.me()
  print 'Got the user name and follower count for ya.\n'
  print ('User Name: %s, Follower Count: %d' % (user.screen_name, user.followers_count))
  while True:
    follower_list = []

    for followers in tweepy.Cursor(api.followers, user.screen_name).items():
      r.sadd('followers', followers.screen_name)

    time.sleep(interval_secs)

    for followers in tweepy.Cursor(api.followers, user.screen_name).items():
      r.sadd('followers_new', followers.screen_name)

    set_diff = r.sdiff('followers', 'followers_new')
    diff = list(set_diff)
    if len(diff) > 0:
      print ('\nUnfollower list for %s \n----------------------------------' % (user.screen_name))
      print diff
      user = api.me()
      print ('\n-->There are %d followers remaining' % (user.followers_count))
    else:
      print 'No unfollower for now..'
    r.delete('followers', 'followers_new')

if __name__ == '__main__':
  main()
