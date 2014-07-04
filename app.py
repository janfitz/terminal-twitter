#!/usr/bin/env python
from keys import *
import webbrowser
import tweepy
import cPickle
import click
import os

USER_FILE = 'user.pkl'
TWEETS_FILE = 'tweets.pkl'
OPTIONS_FILE = 'options.pkl'

@click.group(invoke_without_command=True)
@click.pass_context
def main(context):
  """A CLI to Twitter with support to display, open and compose tweeets"""
  if context.invoked_subcommand is None:
    get_tweets()

def authenticate():
  """Authenticate the user"""
  try:
    auth=load_user()
  except:
    auth = save_user()
  return tweepy.API(auth)
  
def load_options():
  """Load the application options from file"""
  with open(OPTIONS_FILE, 'r') as f:
    return cPickle.load(f)

def save_options(options):
  """Save the application options in a file"""
  with open(OPTIONS_FILE, 'wb') as f:
    cPickle.dump(options, f, cPickle.HIGHEST_PROTOCOL)

def load_user():
  """Load the user authentication details file"""
  with open(USER_FILE, 'r') as f:
    return cPickle.load(f)

def save_user():
  """Save the user authentication details in a file"""
  auth = tweepy.OAuthHandler(API_KEY, API_SECRET,'http://sidverma.net/tt/callback')
  try:
    redirect_url = auth.get_authorization_url()
  except tweepy.TweepError:
    click.secho('Error - Failed to get request token.', fg="red")
  print redirect_url
  verifier = raw_input('Verifier:')
  try:
    auth.get_access_token(verifier)
    with open(USER_FILE, 'wb') as f:
      cPickle.dump(auth, f, cPickle.HIGHEST_PROTOCOL)
  except tweepy.TweepError:
    click.secho('Error - Failed to get access token.', fg="red")
  return auth

def delete_user():
  """Remove the user file"""
  os.remove('USER_FILE')

def load_tweets():
  """Load the last saved tweets details file"""
  with open(TWEETS_FILE, 'r') as f:
    return cPickle.load(f)

def save_tweets(tweets):
  """Save the user loaded tweets in a file"""
  with open(TWEETS_FILE, 'wb') as f:
    cPickle.dump(tweets, f, cPickle.HIGHEST_PROTOCOL)

def print_home_timeline(tweets):
  """Print the home timeline of the user"""
  save_tweets(tweets)
  s=""
  for i,tweet in enumerate(tweets):  
    s += ((click.style('[%d] ' %(i+1), bold=True, fg="blue") + 
           click.style('@%s - ' %tweet.author.screen_name, bold=True, fg="cyan") + 
           click.style('%s' %tweet.text)).encode('utf_8')+'\n\n')
  click.echo_via_pager(s)

@main.command()
@click.option('--media', is_flag=True)
def compose(media):
  """Composes a tweet"""
  api = authenticate()
  if media:
    media = click.prompt('Enter the media path').encode('utf_8')
    media = media.strip(' ')
    media = media.strip('\'')
    x=open(media,'r')
    tweet = click.prompt('Enter the tweet')
    api.update_with_media(filename='a.png',status=tweet,file=x)
  else:
    tweet = click.prompt('Enter the tweet')
    api.update_status(tweet)
  click.echo('Your tweet has been published')

def reply():
  """Retweet to a given tweet"""

def retweet():
  """Retweet a given tweet"""

def favorite():
  """Favorite a tweet"""

def browse_tweet():
  """Opens the tweet in web browser"""

def get_tweets():
  """Display the user's Twiter feed"""
  api = authenticate()
  try:
    print_home_timeline(api.home_timeline(count=25))
  except Exception as e:
    click.secho('Error - Unable to connect to Twitter.\n%s' %e, fg="red")

if __name__ == '__main__':
  main()
