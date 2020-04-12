import sys
import json
import os
from src.data.DatasetGenerator import generateDataset

def main(targets):

	if "gen-data" in targets:
		configPath = './config/datasetGenConfig.json'
		with open(configPath) as f:
			config = json.load(f)
		f.close()
		generateDataset(config)


	pass

if __name__ == '__main__':
	targets = sys.argv[1:]
	main(targets)