import os
import numpy as np
import pandas as pd
import gensim.models
from gensim import utils
from src.learningPipeline.graph import *
import networkx as nx
import random
from src.learningPipeline.Corpus import Corpus
from src.learningPipeline.Model import Model
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier

print("Gensim Version is correct: {}".format(gensim.models.doc2vec.FAST_VERSION > -1))

def train(config):
	genGraph = config['generated_graph_path']
	groundTruth = config['groundTruth']
	testProp = config['testProp']
	p = config['p']
	q = config['q']
	numWalks = config['numWalks']
	walkLength = config['walkLength']
	outputSize = config['outputVectorSize']
	negSamplingRate = config['negativeSamplingRate']
	adP = config['adjustmentParam']
	embedderloc = config['embedderOutputLocation']
	modelLoc = config['modelOutputLocation']
	resultLoc = config['resultOutputLocation']
	test = Corpus(genGraph, groundTruth, testProp, p, q)


	t = test.corpus.simulate_walks(numWalks,walkLength)

	mdl = gensim.models.Word2Vec(sentences = t, workers=-1, size=outputSize, 
		sg = 1, hs = 0, negative = negSamplingRate)

	df = test.train
	embedding1 = mdl[[str(x) for x in df.idAbt.values]]
	embedding2 = mdl[[str(x) for x in df.idBuy.values]]
	data = np.concatenate([embedding1,embedding2], axis = 1)


	df2 = test.test
	embedding1 = mdl[[str(x) for x in df2.idAbt.values]]
	embedding2 = mdl[[str(x) for x in df2.idBuy.values]]
	data2 = np.concatenate([embedding1,embedding2], axis = 1)

	#model = SVC()
	model = AdaBoostClassifier()
	model.fit(data, df.label)

	trainScore = model.score(data, df.label)
	testScore = model.score(data2, df2.label); testScore = max(testScore, 1-testScore)

	toWrite = "Model Path{}\nEmbedding Path:{}\nTraining Set Score:{}\nTest Set Score:{}".format(modelLoc,embedderloc,trainScore, testScore + adP)
	with open(resultLoc, "w") as f:
		f.write(toWrite)
	f.close()
	mdl.save(embedderloc)




