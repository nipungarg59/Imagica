from __future__ import division
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
import math
import numpy as np
import sys
from . import path_len_sim, m2, tfidf
import pandas as pd 
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import style
from collections import Counter 
import plotly.plotly as py
import datetime, hashlib, os, random 
style.use('fivethirtyeight')


FILE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = FILE_DIR + "/djreact/static/images/"

def analysis(str1, str2):
	print(str1, str2)
	data = {
		'Tf-Idf' : tfidf.cosine_sim(str1,str2),
		'Indexing' : m2.similarity(str1,str2),
		'Distribution-F' : path_len_sim.similarity(str1,str2,False),
		'Distribution-T' : path_len_sim.similarity(str1,str2,True)
	}

	objects = ('Tfidf', 'Lsi', 'Dist-f', 'Dist-t')
	y_pos = np.arange(len(objects))
	performance = [data['Tf-Idf'], data['Indexing'], data['Distribution-F'], data['Distribution-T']]
	 
	plt.bar(y_pos, performance, align='center', alpha=0.5)
	plt.xticks(y_pos, objects)
	plt.ylabel('Similarity')
	plt.title('Analysis of Semantic Similarity')
	random_str = str(hashlib.sha1(os.urandom(128)).hexdigest())[:32]
	image_name = STATIC_DIR + random_str + '.png'
	plt.savefig(image_name)
	for key in data:
		data[key] = str(data[key])
	
	import base64
	with open(image_name, "rb") as image_file:
		encoded_string = base64.b64encode(image_file.read())
	data['image_url'] = "data:image/png;base64, "+encoded_string

	return data