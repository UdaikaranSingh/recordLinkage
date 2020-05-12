from src.FeatureExtraction.GraphEmbedder import graphEmbedder
import pandas as pd
import numpy as np
import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import re

def fixPrice(x):
    if not (type(x)== float):
        try:
            return re.findall("\d+\.\d+", x)[0]
        except:
            return np.nan
    else:
        return x

def build_abt_buy_graph(config):
	outpath = config['outpath']
	bins = config["bins"]
	name_min_df = config['name_min_df']
	text_min_df = config['text_min_df']

	pt1 = "./data/Abt-Buy/Abt.csv"
	pt2 = "./data/Abt-Buy/Buy.csv"
	pt3 = "./data/Abt-Buy/abt_buy_perfectMapping.csv"

	Abt = pd.read_csv(pt1, engine = 'python')
	Buy = pd.read_csv(pt2, engine = 'python')
	truth = pd.read_csv(pt3)

	Abt['price'] = pd.to_numeric(Abt.price.apply(fixPrice))
	Buy['price'] = pd.to_numeric(Buy.price.apply(fixPrice))

	gE = graphEmbedder()

	gE.defineKeys(Abt, 'id')
	gE.defineKeys(Buy, 'id')

	gE.defineTruth(truth)

	gE.embeddText([Abt,Buy], 'id','name','name', min_df=name_min_df)

	gE.embeddText([Abt,Buy], 'id','description','description', min_df = text_min_df)

	gE.embeddOrdinal([Abt,Buy],'id','price','price', bins = bins)

	gE.embeddCategorical([Buy], 'id', 'manufacturer', 'manufacturer')

	gE.saveGraph(fname = os.path.join(outpath,"abt_buy_graph.csv"))

def build_dblp_acm_dataset(config):

	outpath = config['outpath']
	bins = config["bins"]
	name_min_df = config['name_min_df']
	text_min_df = config['text_min_df']

	pt1 = "./data/DBLP-ACM/DBLP2.csv"
	pt2 = "./data/DBLP-ACM/ACM.csv"
	pt3 = "./data/DBLP-ACM/DBLP-ACM_perfectMapping.csv"

	dblp2 = pd.read_csv(pt1, engine = 'python')
	acm = pd.read_csv(pt2)
	matchings = pd.read_csv(pt3)

	gE = graphEmbedder()

	gE.defineKeys(dblp2, 'id')
	gE.defineKeys(acm, 'id')
	gE.defineTruth(matchings)

	gE.embeddText([dblp2,acm], 'id','title','title', min_df=name_min_df)
	gE.embeddText([dblp2,acm], 'id','authors','authors', min_df=name_min_df)

	gE.embeddCategorical([dblp2,acm], 'id', 'venue', 'venue')
	gE.embeddCategorical([dblp2,acm], 'id', 'year', 'year')

	gE.saveGraph(fname =os.path.join(outpath,"dblp_acm_graph.csv"))

def build_dblp_scholar_dataset(config):

	outpath = config['outpath']
	bins = config["bins"]
	name_min_df = config['name_min_df']
	text_min_df = config['text_min_df']


	pt1 = "./data/DBLP-Scholar/DBLP1.csv"
	pt2 = "./data/DBLP-Scholar/Scholar.csv"
	pt3 = "./data/DBLP-Scholar/DBLP-Scholar_perfectMapping.csv"

	dblp1 = pd.read_csv(pt1, engine = 'python')
	scholar = pd.read_csv(pt2)
	matchings = pd.read_csv(pt3)

	gE = graphEmbedder()

	print("checkpoint 1")
	gE.defineKeys(dblp1, 'id')
	gE.defineKeys(scholar, 'id')
	gE.defineTruth(matchings)

	print("checkpoint 2")
	gE.embeddText([dblp1,scholar], 'id','title','title', min_df=text_min_df)
	print("checkpoint 3")
	gE.embeddText([dblp1,scholar], 'id','venue','venue', min_df=text_min_df)
	print("checkpoint 4")
	gE.embeddText([dblp1,scholar], 'id','authors','authors', min_df=name_min_df)
	print("checkpoint 5")

	gE.embeddCategorical([dblp1,scholar], 'id', 'year', 'year')

	gE.saveGraph(fname =os.path.join(outpath,"dblp_scholar_graph.csv"))

def build_amazon_google_dataset(config):

	outpath = config['outpath']
	bins = config["bins"]
	name_min_df = config['name_min_df']
	text_min_df = config['text_min_df']


	pt1 = "./data/Amazon-GoogleProducts/Amazon.csv"
	pt2 = "./data/Amazon-GoogleProducts/GoogleProducts.csv"
	pt3 = "./data/Amazon-GoogleProducts/Amzon_GoogleProducts_perfectMapping.csv"

	amazon = pd.read_csv(pt1, engine = 'python')
	google = pd.read_csv(pt2, engine = 'python')
	matchings = pd.read_csv(pt3)

	google = google.rename(columns={'name':'title'})

	google.price = pd.to_numeric(google.price.apply(fixPrice))

	gE = graphEmbedder()

	gE.defineKeys(amazon, 'id')
	gE.defineKeys(google, 'id')
	gE.defineTruth(matchings)

	gE.embeddText([amazon,google], 'id','title','title', min_df=name_min_df)
	gE.embeddText([amazon,google], 'id','description','description', min_df=text_min_df)

	gE.embeddCategorical([amazon,google], 'id','manufacturer','manufacturer')

	gE.embeddOrdinal([amazon,google], 'id','price','price')

	gE.saveGraph(fname =os.path.join(outpath,"amazon_google_graph.csv"))
