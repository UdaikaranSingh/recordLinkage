import pandas as pd
import numpy as np
import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import re

class graphEmbedder:
    
    def __init__(self):
        self.entityNodes = set()
        self.Graphs = []
    
    def defineKeys(self,df,idCol):
        temp = set(df[idCol])
        self.entityNodes.update(temp)
    
    def embeddOrdinal(self,dfs,idCol,column,name,bins=10, equalBinSize = True):
        df = pd.concat([df[[idCol,column]] for df in dfs])
        if equalBinSize: temp = pd.qcut(df[column], q = bins, labels = False)
        else: temp = pd.cut(df[column], bins = bins, labels = False)
        
        tempDf = df[[idCol]].copy(deep=True)
        tempDf['temp'] = temp
        graph = dict(tempDf.dropna().to_numpy())
        self.Graphs.append((name,graph))
        return True
    
    def embeddText(self,dfs,idCol, column,name, min_df = 0.01, method = 'BagOfWords'):
        df = pd.concat([df[[idCol,column]] for df in dfs])
        temp = df[[idCol, column]]
        temp = temp.dropna()
        if method == 'BagOfWords': vectorizer = CountVectorizer(min_df=min_df,max_df = 0.7, ngram_range = (1,1),max_features = 10000)
        elif method == 'TFIDF': vectorizer = TfidfVectorizer(min_df=min_df,max_df = 0.7, ngram_range = (1,1), max_features = 10000)
        
        output = vectorizer.fit_transform(temp[column]).toarray()
        print(output.shape)
        tokens = vectorizer.get_feature_names()
        idVal = list(temp[idCol])
        
        graph = {}
        for i in range(output.shape[0]):
            words = []
            for j in range(output.shape[1]):
                if output[i][j] > 0:
                    words.append(tokens[j])
            graph[idVal[i]] = words
        
        self.Graphs.append((name,graph))
        return True
    
    def embeddCategorical(self,dfs,idCol,column,name):
        df = pd.concat([df[[idCol,column]] for df in dfs])
        graph = dict(df[[idCol,column]].to_numpy())
        self.Graphs.append((name,graph))
        return True
    
    def defineTruth(self, df):
        graph = dict(df.to_numpy())
        self.Graphs.append(('ground_truth',graph))
        return True
    
    def saveGraph(self, method = 'csv', fname = 'heteroGraph.csv'):
        df = pd.DataFrame(columns = ['source', 'target','type'])
        print(len(self.Graphs))
        for graph in self.Graphs:
            name = graph[0]
            links = graph[1]
            data = self._graphFixer(links)
            temp = pd.DataFrame(data = data, columns = ['source', 'target'])
            temp['type'] = name
            
            df = pd.concat([df, temp])
        df.to_csv(os.path.join(os.getcwd(),fname), index = False)
    
    def _graphFixer(self, dictionary):
        temp = []
        for key, value in dictionary.items():
            
            if type(value)==list:
                for v in value:
                    temp.append((key,v))
            else:
                temp.append((key,value))
            
        return temp