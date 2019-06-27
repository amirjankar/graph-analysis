# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 15:05:02 2018

@author: charl
"""

from BagOfWords import bagOfWords
import pickle
import pandas as pd

classBag = pickle.load(open('classificationBag.pickledfile','rb'))
sentBag = pickle.load(open('sentimentBag.pickledfile','rb'))
data = pd.read_csv('verified.csv')
data['sentiment'] = ''
data['classification'] = ''
data = data.drop('Unnamed: 0', axis=1)
data['sentiment'] = data.apply(lambda row: sentBag.classify_string(row['content'])[0], axis = 1)
data['classification'] = data.apply(lambda row: classBag.classify_string(row['content'])[0], axis = 1)


data.to_csv('verified_classified.csv')