from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords,wordnet
from nltk.stem import WordNetLemmatizer
from itertools import product
import numpy






 

##---------------Defining stopwords for English Language---------------##
stop_words = set(stopwords.words("english"))

##---------------Initialising Lists---------------##
filtered_sentence1 = []
filtered_sentence2 = []
lemm_sentence1 = []
lemm_sentence2 = []
sims = []
temp1 = []
temp2 = []
simi = []
final = []
same_sent1 = []
same_sent2 = []
#ps = PorterStemmer()

##---------------Defining WordNet Lematizer for English Language---------------##
lemmatizer  =  WordNetLemmatizer()


def preprocess(str,filtered_sentence,lemm_sentence):
  for words1 in word_tokenize(str):
    if words1 not in stop_words:
      if words1.isalnum():
        filtered_sentence.append(words1)

  for i in filtered_sentence:
    lemm_sentence.append(lemmatizer.lemmatize(i))

  return lemm_sentence


def similarity(str1,str2):
  lemm_sentence1=preprocess(str1,[],[])
  lemm_sentence2=preprocess(str2,[],[])
  for word1 in lemm_sentence1:
    simi =[]
    for word2 in lemm_sentence2:
        sims = []
       # print(word1)
        #print(word2)
        syns1 = wordnet.synsets(word1)
        #print(syns1)
        #print(wordFromList1[0])
        syns2 = wordnet.synsets(word2)
        #print(wordFromList2[0])
        for sense1, sense2 in product(syns1, syns2):
            d = wordnet.wup_similarity(sense1, sense2)
            if d != None:
                sims.append(d)
    
        #print(sims)
        #print(max(sims))
        if sims != []:        
           max_sim = max(sims)
           #print(max_sim)
           simi.append(max_sim)
             
    if simi != []:
        max_final = max(simi)
        final.append(max_final)

  similarity_index = numpy.mean(final)
  similarity_index = round(similarity_index , 2)
  return similarity_index










#print(similarity(str1,str2))
