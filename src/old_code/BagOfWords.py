# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 00:01:41 2018

@author: charl
"""

import nltk
import math
import copy

#References I pulled from:
#machinelearningmastery.com/gentle-introduction-bag-words-model/
#wikipedia.org/wiki/Bag-of-words-model

#NOTES
# * This runs quickly enough on small amounts of data but hasn't been tested on large amounts
# * You need to have a list of strings ready and labeled for each category
# * Its confidence in its classification will go down as the number of categories goes up
# * It recalculates all its information whenever a new category is added
# * The model assumes all categories are equally likely, basing predictions solely on contents

class bagOfWords:
    
    #Add a category; it takes the title of the category and a list of strings
    #The strings should just be a list of strings in that category
    #Whenever a string is added it recalculates the bag
    def add_category(self, title, str_list):
        self.num_categories = self.num_categories + 1
        new_dict = {}
        bag_size = 0
        for x in str_list:
            bag_size = bag_size + 1
            
            tokens = nltk.word_tokenize(x.lower())
            for y in tokens:
                if y in new_dict:
                    new_dict[y] = new_dict.get(y) + 1
                else:
                    new_dict[y] = 1
                if y in self.all_words:
                    self.all_words[y] = self.all_words.get(y) + 1
                else:
                    self.all_words[y] = 1
                    
        final_dict = {}
        final_dict["Title"] = title
        final_dict["Data"] = new_dict
        final_dict["Size"] = bag_size
        self.bags.append(final_dict)
        self.__recalc_bags__()
        
    #Removes a bag from the list and recalculates everything
    #Cannot be undone etc
    def del_category(self, title):
        self.num_categories = self.num_categories-1
        remBag = None
        for x in self.bags:
            if x.get('Title') == title:
                remBag = x
        assert remBag is not None, 'Title not found'
        
        for x in remBag.get('Data'):
            self.all_words[x] = self.all_words[x] - remBag['Data'][x]
            if self.all_words[x] == 0:
                self.all_words.pop(x)
        
        self.bags.remove(remBag)
        self.__recalc_bags__()
    
    #Fairly straightforward, if you have at least 1 categories it takes a string
    #And does its best to classify that string
    #It also returns a % of how sure it is in its assesment
    def classify_string(self, input_str):
        assert self.num_categories >= 1, "Need at least 1 categories for any categorization"
        tokens = nltk.word_tokenize(input_str.lower())
        maxVal = -1
        allVal = 0
        maxName = ''
        for x in self.bags:
            currVal = self.__string_val__(tokens, x)
            allVal = allVal + currVal
            if currVal > maxVal:
                maxVal = currVal
                maxName = x.get('Title')
        if allVal == 0:
            allVal = 1
            maxVal = 1
        return maxName, (maxVal/allVal)
        
        
    #Finds the value of a string when in a certain bag
    def __string_val__(self, tokens, bag):
        val = 0
        data = bag.get('Vals')
        for x in tokens:
            if x in data:
                val = val + data[x]
        return val
        
    #Goes through all bags and calculates (or recalculates) the values
    #This performs tfidf on all of the words in each bag
    def __recalc_bags__(self):
        for bag in self.bags:
            data = copy.deepcopy(bag.get('Data'))
            for entry in data:
                data[entry] = self.__tfidf__(entry, bag)
            bag["Vals"] = data
            
        
    #CA/alculates the tf-idf significance of a word in a bag  
    def __tfidf__(self, term, bag):
        bagData = bag.get('Data')
        assert term in bagData, 'Terms must be in a bag for tf-idf'
        tf = bagData.get(term)
        numCont = 0
        for x in self.bags:
            if term in x.get('Data'):
                numCont = numCont + 1
        idf = math.log(self.num_categories/numCont)
        return tf * idf
    
    def __init__(self):
        self.num_categories = 0
        self.all_words = {}
        self.bags = []
            


#bagTest = BagOfWords()     
#boring = ["I went to the market today", "Weather happens sometimes", "I like the color beige", "I got bored of being bored", "Will you be at the fair?", "Sometimes things occurr"]
#exciting = ['WHOA', 'Man sometimes things are wild!', 'It\'s crazy over here at the market', 'Things are heating up!', 'Dude you are missing out on this, get over here']
#bagTest.add_category('boring', boring)
#bagTest.add_category('exciting', exciting)
#testStr = 'MAN it is so cold out, I love it'
#bag_class, prob = bagTest.classify_string(testStr)
#print('The string is classified as "' + bag_class +'", its confidence in that prediction is ' + str(prob))
#bagTest.del_category('exciting')
#bag_class, prob = bagTest.classify_string(testStr)
#print('The string is classified as "' + bag_class +'", its confidence in that prediction is ' + str(prob))
