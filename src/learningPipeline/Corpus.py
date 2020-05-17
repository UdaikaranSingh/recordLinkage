import os
import numpy as np
import pandas as pd
import gensim.models
from gensim import utils
from src.learningPipeline.graph import *
import networkx as nx
import random

class Corpus:
    
    def __init__(self, pt, groundTruth, testProp, p, q):
        self.path = pt
        print('building train/test sets')
        self.build(pt, testProp,groundTruth)
        self.p = p
        self.q = q
        print('building graph')
        self.generateCorpus()
        
        pass
    
    def build(self, pt, testProp, groundTruth):
        #note: temp1 is the training/test set; temp2 is the graph
        df = pd.read_csv(pt).astype(str) 
        temp1 = pd.read_csv(groundTruth)
        print(list(temp1.columns))
        temp1 = self.generateNegativeSamples(temp1)
        self.trainTestSplit(temp1, testProp)
        self.buildGraph(df)
    
    def generateNegativeSamples(self,df):
        df['label'] = 1
        col1 = df.columns[0]
        col2 = df.columns[1]
        allItems = set(df[col1])
        negSamples = []
        for i, row in df.iterrows():
            source = row[col1]
            target = row[col2]
            negSamples.append((source, random.sample(allItems.difference(set([target])), 1)[0]))
        t = pd.DataFrame(negSamples, columns = [col1,col2])
        t['label'] = 0
        return pd.concat([t, df])
    
    
    def trainTestSplit(self, df, testProp):
        df = df.sample(len(df))
        nodes = set(df[df.columns[1]].values)
        nodes.update(set(df[df.columns[0]].values))
        self.nodes = [str(x) for x in list(nodes)]
        cutoff = int(len(df) * testProp)
        test = df.iloc[0:643]
        train = df.iloc[643:]
        self.train = train
        self.test = test
    
    def buildGraph(self, df):
        G=nx.Graph()
        
        temp = set([str(x) for x in df['source']])
        temp.update(set([str(x) for x in df['target']]))
        edges = tuple(zip([str(x) for x in list(df['source'])], [str(x) for x in list(df['target'])]))
        G.add_nodes_from(temp)
        G.add_edges_from(edges, weight = 1)
        self.G = G
    
    def generateCorpus(self):
        self.corpus = Graph(self.G, self.nodes, is_directed= False, p = self.p, q = self.q)
        self.corpus.preprocess_transition_probs()