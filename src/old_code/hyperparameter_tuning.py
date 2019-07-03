# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 16:48:14 2018

@author: charl
"""

from RandomForestDriver import RandomForest
import pandas as pd

train_data = pd.read_csv('final_data.csv')
train_labels = train_data['retweet_count']
train_data = train_data.drop(['retweet_count'], axis=1)
test_data = pd.read_csv('Final_Test_Data.csv')
test_labels = test_data['retweet_count']
test_data = test_data.drop(['retweet_count'], axis=1)

max_count = 100

perim = int(max_count/2)
pt1 = int(perim/2)
pt2 = int(pt1 + perim)

while pt1 != pt2:
    forest = RandomForest(pt1)
    forest.train(train_data, train_labels)
    
    err1 = 0
#    for i, data_point in enumerate(test_data):
#        if forest.predict(test_data, True) != test_labels[i]:
#            err1 = err1 + 1
    
    for i in test_data.iterrows():
        index, row = i
        if forest.predict(row, True) != test_labels[index]:
            err1 = err1 + 1
            
            
    forest = RandomForest(pt2)
    forest.train(train_data, train_labels)
    
    err2 = 0
#    for i, data_point in enumerate(test_data):
#        if forest.predict(test_data, True) != test_labels[i]:
#            err2 = err2 + 1
    for i in test_data.iterrows():
        index, row = i
        if forest.predict(row, True) != test_labels[index]:
            err2 = err2 + 1
            
    print('Pt1: ', str(pt1), ', Err: ', str(err1))
    print('Pt2: ', str(pt2), ', Err: ', str(err2))
    
    if err1 > err2:
        cent = pt2
    else:
        cent = pt1
        
    perim = int((perim-1)/2)
    pt1 = cent - perim
    pt2 = cent + perim



#forest.train(data, labels, bootstrapping=True)
