# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 17:43:17 2018

@author: charl
"""

import tkinter as tk
from tkinter import END
import pickle
import pandas as pd
from RandomForestDriver import RandomForest
from BagOfWords import bagOfWords

#Get the bags of words and the forest
f = open('sentimentBag.pickledfile', 'rb')
sentBag = pickle.load(f)
f = open('classificationBag.pickledfile', 'rb')
classBag = pickle.load(f)
f = open('forest.cooltimes', 'rb')
forest = pickle.load(f)

def classifyText(text):
    return classBag.classify_string(text)

def sentimentText(text):
    return sentBag.classify_string(text)

def decodeForestVal(val):
    if val == 1:
        return('Lots of retweets!')
    if val == .5:
        return('Above average')
    return('Average to low')
    
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
    
def forestClassify(num_following, num_followers, num_tweets, text):
    testDat= {}
    testDat['following'] = num_following
    testDat['followers'] = num_followers
    testDat['tweets_count'] = num_tweets
    testDat['sentiment'] = classifySentiment(sentimentText(text)[0])
    testDat['classification'] = classifyType(classifyText(text)[0])
    test = pd.Series(testDat)
    return(decodeForestVal(forest.predict(test, True)))
    

class Window(tk.Frame):
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_window()        
        
    def init_window(self):
        self.master.title('Tweet predictor')
        
        def calcTot():
            followingCount = int(followingEntry.get())
            followedCount = int(followedEntry.get())
            tweetsCount = int(numTweetsEntry.get())
            tweet = str(tweetEntry.get())
            ans = forestClassify(followingCount, followedCount, tweetsCount, tweet)
            resultText.config(state=tk.NORMAL  )
            resultText.delete(1.0,tk.END)
            resultText.insert(tk.INSERT,ans)
            resultText.config(state=tk.DISABLED)
            followingEntry.delete(0,tk.END)
            followingEntry.insert(tk.INSERT,'# of people you follow')
            followedEntry.delete(0,tk.END)
            followedEntry.insert(tk.INSERT,'# of people following you')
            numTweetsEntry.delete(0,tk.END)
            numTweetsEntry.insert(tk.INSERT,'# of tweets you\'ve made')
            tweetEntry.delete(0,tk.END)
            tweetEntry.insert(tk.INSERT,'A tweet!')
            
            
        
        instructText = tk.Text(root, width=55, height=5 )
        instructText.insert(tk.INSERT, 'Instructions')
        instructText.insert(tk.INSERT, '\nWelcome to my ugly gui I hope you love it')
        instructText.insert(tk.INSERT, '\nType your tweet in the box, size limit not enforced')
        instructText.insert(tk.INSERT, '\nFill in the other parameters')
        instructText.insert(tk.INSERT, '\nPush "Run" to calculate"')
        instructText.config(state=tk.DISABLED)
        instructText.pack(pady=20)
        
        followingEntry = tk.Entry(root)
        followingEntry.pack(side='left', padx=10)
        followingEntry.delete(0,tk.END)
        followingEntry.insert(0, '# of people you follow')

        followedEntry = tk.Entry(root)
        followedEntry.pack(side='left', padx=10)
        followedEntry.delete(0,tk.END)
        followedEntry.insert(0, '# of people following you')
                             
        
        numTweetsEntry = tk.Entry(root)
        numTweetsEntry.pack(side='left', padx=10)
        numTweetsEntry.delete(0,tk.END)
        numTweetsEntry.insert(0, '# of tweets you\'ve made')
                              

        tweetEntry = tk.Entry(root)
        tweetEntry.pack(padx=15, pady=20)
        tweetEntry.delete(0,tk.END)
        tweetEntry.insert(0, 'A tweet!')
                              
        
        runButton = tk.Button(text='Run', width='80', height='10', command=calcTot)
        runButton.pack(padx=15, pady=20)
            
        
        #The text which shows the result
        resultText = tk.Text(root, width=20, height=1)
        resultText.insert(tk.INSERT, 'Result')
        resultText.configure(state=tk.DISABLED)
        resultText.pack(side='bottom', padx=15, pady=20)
        
        
        
def ask_quit():
    root.destroy()
              
root = tk.Tk()
root.protocol('WM_DELETE_WINDOW', ask_quit)
frame= tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=1) 
#root.geometry('400x400')
app = Window(root)
root.mainloop()        