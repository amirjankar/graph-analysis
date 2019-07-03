import pandas as pd, numpy, math, random, DecisionTree
from collections import Counter


"""
@author: anmirjan
"""
class RandomForest:
    """
    Creates random forest from a decision tree
    Trains model based on given dataset

    """
    def __init__(self, count=5):
        
        testDat= {}
        testDat['following'] = 0
        testDat['followers'] = 0
        testDat['tweets_count'] = 0
        testDat['sentiment'] = 0
        testDat['classification'] = 0
        tmp = pd.DataFrame(testDat, index = [0])
        tmp = tmp.drop(0)
        
        self.data = {i:tmp.copy() for i in range(count)}
        self.labels = {i:[] for i in range(count)}
        self.forest = [None for i in range(count)]
        self.count = count
        
    
    def round_to(self, n, prec):
        return prec * int( n/prec+.5 )
    
    def round_to_5(self, n):
        return self.round_to(n, 0.05)



    def train(self, data, labels, bootstrapping = True):
#        for i, data in enumerate(data):
        

        for i in data.iterrows():
            index, rowdata = i
            assigned_tree = math.floor(random.random() * self.count)
            # adds key value pair to data, labels
    #       self.data[assigned_tree].append((index, rowdata))
            self.data[assigned_tree] = self.data[assigned_tree].append(rowdata)
            self.labels[assigned_tree].append((index, labels[index]))
        if bootstrapping:
            treesPerForest = int(len(data)/3)
            for i in range(0, self.count):
                data = data.sample(frac=1)
                self.data[i] = self.data[i].append(data.iloc[1:treesPerForest, :])
                index = data.index.values.astype(int)[1:treesPerForest]
                for r in index:
                    self.labels[i].append((r, labels[r]))
            

        for i, tree in enumerate(self.forest):
            x = pd.DataFrame(self.labels[i]).drop(0, axis=1)
            self.forest[i] = DecisionTree.DecisionTree(self.data[i].reset_index(drop=True), x.squeeze())
            self.forest[i].build_tree()

    def predict(self, data, distinct):
        output = []
        output = [dt.classify(data) for dt in self.forest]
        print(output)
#        for x in self.forest:
#            output.append(x.classify(data))
            
        if distinct:
            return [word for word, word_count in Counter(output).most_common(2)][0]
        return self.round_to_5(sum(output)/len(output))
    

if __name__ == "__main__":
    forest = RandomForest(count = 49)

    ## train forest
    csv_data = pd.read_csv('final_data.csv')
    labels = csv_data['retweet_count']
    data = csv_data.drop(['retweet_count'], axis=1)

    forest.train(data, labels, bootstrapping=True)

    # prediction
#    test_data = pd.read_csv('verified_test.csv')
#    labels = test_data['retweet_count']
#    data = test_data.drop(['retweet_count'])
    
    testDat= {}
    testDat['following'] = 62620
    testDat['followers'] = 5987
    testDat['tweets_count'] = 43101
    testDat['sentiment'] = -1
    testDat['classification'] = .8
    test = pd.Series(testDat)
    forest.predict(test, True)
    
    

#    for i, data_point in enumerate(data):
#        assert forest.predict(data) is labels[i]

    print("Completed")
    
    td = pd.read_csv('Final_Test_Data.csv')
    incorrect = 0
    
    for x in range(0, len(td)):
        row = td.iloc[x]
        val = row['retweet_count']
        row = row.drop('retweet_count')
        
        
        retVal = forest.predict(row, True)
        if retVal != val:
            incorrect = incorrect + 1
        
        print('Real: ', str(val), 'Discovered: ', str(retVal), 'err rate so far: ', str(incorrect))
        
    print("Error rate:  " + str(incorrect/len(td)))
    
    
    
    
    
    