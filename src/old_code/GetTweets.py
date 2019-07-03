# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 17:55:55 2018

@author: charl
"""

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream, API, TweepError, Cursor, Status, User
import json
import pandas as pd
import time
from urllib3.exceptions import ProtocolError

class TweetMgr():
    #The authorization and the number of tweets woo
    auth = None    
    numTweets = 0
    
    #This is a listener which you don't have to worry about
    #It just works, not much need said
    class StdOutListener(StreamListener):
        numStatuses = 0
        numTweets = 0
        filterRetweets = False
        x = []
        
        #This organizes data in the listener so it doesn't have to happen later
        #If you're filtering retweets, this is where those tweets are removed
        def formatData(self, tweet):
            try:
                #GEt the tweet and find the flags which it filters along
                a = json.JSONDecoder().decode(tweet)
                
                retweeted = a.get('retweeted')
                user_replied = a.get('in_reply_to_user_id')
                status_replied = a.get('in_reply_to_status_id')
                name_replied = a.get('in_reply_to_screen_name')
                lang = a.get('lang')
                text = a.get('text')
                
                #If filtering retweets and replies
                if (self.filterRetweets and
                    retweeted == False and
                    user_replied is not None and
                    status_replied is not None and
                    name_replied is not None and
                    lang == 'en' and
                    text[0] != '@'):
                
                    tweetID = a.get('id')
                    fav_count = a.get('favorite_count')
                    retweet_count = a.get('retweet_count')
                    userFULL = a.get('user')
                    name = userFULL.get('screen_name')
                    user_loc = userFULL.get('location')
                    user_friends = userFULL.get('users_count')
                    user_followers = userFULL.get('followers_count')
                    user_statuses = userFULL.get('statuses_count')
                    user_verified = userFULL.get('verified')
                    retVal = [tweetID, text, fav_count, retweet_count, 
                              name, user_loc, user_friends, user_followers, user_statuses, user_verified]
                    return retVal
                
                #If not filtering retweets and replies
                elif self.filterRetweets == False:
                    tweetID = a.get('id')
                    fav_count = a.get('favorite_count')
                    retweet_count = a.get('retweet_count')
                    userFULL = a.get('user')
                    name = userFULL.get('screen_name')
                    user_loc = userFULL.get('location')
                    user_friends = userFULL.get('users_count')
                    user_followers = userFULL.get('followers_count')
                    user_statuses = userFULL.get('statuses_count')
                    user_verified = userFULL.get('verified')
                    retVal = [tweetID, text, fav_count, retweet_count, 
                              name, user_loc, user_friends, user_followers, user_statuses, user_verified]
                    return retVal
                
                return None
            except:
                return None
        
        def on_data(self, data):
            #Loads in a tweet, and formats it
            #If it's properly formatted and passes any filter it's added
            #The counter is incremented
            val = self.formatData(data)
            if val is not None:
                self.x.append(val)
                self.numStatuses = self.numStatuses + 1
                print(' * ' + str(self.numStatuses) + ' filtered statuses loaded')
            if self.numStatuses < self.numTweets:
                return True
            else:
                return False
    
        def on_error(self, status):
            print(status)
                        
        def retData(self):
            return self.x
        
        def __init__(self, numTweets, filterRetweets):
            self.numTweets = numTweets
            self.filterRetweets = filterRetweets
            
    
    #This gets the new retweets and favorites from a single tweet given its id
    def getNewStats(self, statusID, api):
        try:
            x = json.dumps(api.get_status(statusID)._json)
            x = json.loads(x)
            ret_count = x.get('retweet_count')
            fav_count = x.get('favorite_count')
    #        print("Updated tweet with ID " + str(statusID))
            return ret_count, fav_count
        #Error handling, special case for rate limit
        except TweepError as t:
            print(' * Tweet with ID ' + str(statusID) + ' error:')
            print(t.reason)
            if t.reason[10:12] == '88' or t.reason[44:46] == '88':
                raise TweepError('Can\'t continue with rate limit exceeded. Wait a bit before trying again')
            return 0,0
    
    #This goes through a given tweets dataframe (formatted as genTweets outputs)
    #It updates the favorites and retweets for each entry
    #It tries to handle rate limiting as well but isn't perfect
    def updateAllStats(self, tweets):
        api = API(self.auth)
        for x in range(0, len(tweets)):
            if x%501 == 0 and x != 0:
                print(" * Pausing for 3 minutes to prevent rate limit exception")
                time.sleep(180)
                print(" * Resuming")
            if x%200 == 0 and x != 0:
                print(' * ' + str(x) + ' tweets formatted')
            try:
                rt, fv = self.getNewStats(tweets.iloc[x,0], api)
            except TweepError:
                print(" * Rate limit exceeded. Waiting 5 minutes before resuming.")
                time.sleep(300)
                rt, fv = self.getNewStats(tweets.iloc[x,0], api)
                
            tweets.iloc[x,2] = fv
            tweets.iloc[x,3] = rt
        print(' * Updated ' + str(x+1) + ' tweets')
    
    #This takes the next tweets posted which contain a bunch of common neutral words
    #Note that at time of taking, they won't have any favorites or retweets
    #This should be update later with updateAllStats    
    def genTweets(self, numTweets, filterRetweets):
        self.numTweets = numTweets
        l = self.StdOutListener(self.numTweets, filterRetweets)
        stream = Stream(self.auth, l)
        
        #Get all the tweets
        contFiltering = True
        while contFiltering:
            try:
                contFiltering = stream.filter(track=['a','the','I','he','she','and','but','or','it','any', 'by',
                                     'not','will','won\'t','be','is','in','has','was','are','of',
                                     'for','can','can\'t'])
            except ProtocolError:
                print("Protocol error: Reconnecting")
                continue
        
        tweets = l.retData()
        tweets = pd.DataFrame(tweets)
        tweets.columns = ['ID', 'text', 'favorite_count', 'retweet_count',
                'username', 'user_loc', 'friends_count', 'followers_count',
                'statuses_count', 'verified']


        return tweets

    # Grabs all tweets from @verified/verified-accounts
    # Eventually grab tweets over a certain number of months
    def getVerifiedTweets(self):
        api = API(self.auth)
        verified_list = api.list_timeline(
            owner_screen_name='@verified',
            slug='verified-accounts',
            count=5000)

        data = []
        for i, page in enumerate(Cursor(
                                    api.list_timeline,
                                    owner_screen_name='@verified',
                                    slug='verified-accounts',
                                    count=200
                                ).pages()):
            total = len(page)
            saved = 0
            for j, tweet in enumerate(page):
                retweeted = tweet.retweeted
                user_replied = tweet.in_reply_to_user_id
                status_replied = tweet.in_reply_to_status_id
                name_replied = tweet.in_reply_to_screen_name
                lang = tweet.lang
                text = tweet.text
                if j < 10:
                    print(lang, ":", text)
                # If filtering retweets and replies
                if not retweeted and 'RT' not in text and lang == "en":

                    user = tweet.user._json
                    saved += 1
                    data.append([
                        tweet.id, tweet.created_at, tweet.text,
                        tweet.favorite_count, tweet.retweet_count,
                        user['screen_name'], user['location'], user['friends_count'],
                        user['followers_count'], user['statuses_count'], user['verified']
                    ])

            print("Page:", i + 1, "- Saved:", saved, "/", total)

        tweets = pd.DataFrame(data)
        tweets.columns = ['id', 'date', 'content', 'retweet_count', 'screen_name',
                          'following', 'followers', 'tweets_count', 'verified']
        print(tweets)

        ## need to figure out pagination & tweets between certain ids, preferably at least a week old
        ## need to filter tweet data and enter into dataframe
        ##  - build data formatter to format tweets coming out of this function
        ##  - figure out some overall pieces to watch, i.e. date range, etc.
        ##  - convert to csv and save

        tweets.to_csv('verified.csv')
    
    #All the oauth funtimes
    #Generates the access needed
    def __init__(self):
       self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token_key, access_token_secret)
        
#Test stuff
print("Creating tweet manager")

x = TweetMgr()
x.getVerifiedTweets()
#numTweets = 8
#print("Generating " + str(numTweets) + " tweets, without retweets")
#tweetDF = x.genTweets(numTweets, True)
#print(tweetDF)
#print("Updating all their stats to current")
#print("When we actually use this we probably won't want to run this immediately after")
#x.updateAllStats(tweetDF)
#print("All done!")
#print(tweetDF)

