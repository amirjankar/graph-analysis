# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 16:24:22 2018

@author: charl
"""

import pandas as pd
import datetime 
import random

def classifySentiment(inpStr):
    if inpStr == 'Negative':
        return -1
    if inpStr == 'Positive':
        return 1
    else:
        return 0
    
def classifyType(inpStr):
    if inpStr == 'Personal':
        return .2
    if inpStr == 'Promotional':
        return .4
    if inpStr == 'Clickbait':
        return .6
    if inpStr == 'News':
        return .8
    else:
        return .99
    
def tweetPop(retw):
    if retw > 1000:
        return 1
    if retw > 200:
        return .5
    return 0
    
def changeDate(currTime, oldTime):
    x = datetime.datetime.strptime(oldTime, '%Y-%m-%d %H:%M:%S')
    return (currTime - x).days

data = pd.read_csv('verified_classified.csv')
data = data.drop('Unnamed: 0', 1)
data = data.drop('content', 1)
data = data.drop('id', 1)
data = data.drop('screen_name', 1)
data = data.drop('verified', 1)
data = data.drop('date', 1)

data['retweet_count'] = data['retweet_count'].apply(tweetPop)
data['sentiment'] = data['sentiment'].apply(classifySentiment)
data['classification'] = data['classification'].apply(classifyType)
currTime = datetime.datetime.now()

maxSmallest = len(data[data['retweet_count'] == 1]) + len(data[data['retweet_count'] == .5])
maxSmallest = int(maxSmallest * .5)
smallestData = data[data.retweet_count == 0]
data = data[data.retweet_count != 0]
data = data.reset_index(drop=True)
smallestData = smallestData.reset_index(drop=True)

while len(smallestData) > maxSmallest:
    smallestData = smallestData.drop(int(random.random()* len(smallestData)), axis=0)
    smallestData = smallestData.reset_index(drop=True)
    
data = data.append(smallestData)
data = data.sample(frac=1).reset_index(drop=True)

cols = ['following', 'followers', 'tweets_count', 'sentiment', 'classification', 'retweet_count']
data = data[cols]
data.to_csv('Final_Test_Data.csv', index=False)

