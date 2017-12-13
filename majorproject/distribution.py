from __future__ import division
import math
import numpy as np
import sys
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from .param import *


def best_syn_pair(word_1, word_2):
    max_sim = -1.0
    synonym_sets_1 = wn.synsets(word_1)
    synonym_sets_2 = wn.synsets(word_2)
    if len(synonym_sets_1) == 0 or len(synonym_sets_2) == 0:
        return None, None
    else:
        max_sim = -1.0
        best_pair = None, None
        for synonym_set_1 in synonym_sets_1:
            for synonym_set_2 in synonym_sets_2:
               sim = wn.path_similarity(synonym_set_1, synonym_set_2)
               if sim > max_sim:
                   max_sim = sim
                   best_pair = synonym_set_1, synonym_set_2
        return best_pair



def length_wise_distribution(synonym_set_1, synonym_set_2):
    length_distribution = sys.maxint
    if synonym_set_1 is None or synonym_set_2 is None: 
        return 0.0
    if synonym_set_1 == synonym_set_2:
        length_distribution = 0.0
    else:
        word_set_1 = set([str(x.name()) for x in synonym_set_1.lemmas()])        
        word_set_2 = set([str(x.name()) for x in synonym_set_2.lemmas()])
        if len(word_set_1.intersection(word_set_2)) > 0:
            length_distribution = 1.0
        else:
            length_distribution = synonym_set_1.shortest_path_distance(synonym_set_2)
            if length_distribution is None:
                length_distribution = 0.0
    return math.exp(-ALPHA * length_distribution)

def hierarchial_wise_distribution(synonym_set_1, synonym_set_2):
    h_dist = sys.maxint
    if synonym_set_1 is None or synonym_set_2 is None: 
        return h_dist
    if synonym_set_1 == synonym_set_2:
        h_dist = max([x[1] for x in synonym_set_1.hypernym_distances()])
    else:
        hypernyms_1 = {x[0]:x[1] for x in synonym_set_1.hypernym_distances()}
        hypernyms_2 = {x[0]:x[1] for x in synonym_set_2.hypernym_distances()}
        subnumers = set(hypernyms_1.keys()).intersection(
            set(hypernyms_2.keys()))
        if len(subnumers) > 0:
            lcs_dists = []
            for subnumer in subnumers:
                lcs_d1 = 0
                if hypernyms_1.has_key(subnumer):
                    lcs_d1 = hypernyms_1[subnumer]
                lcs_d2 = 0
                if hypernyms_2.has_key(subnumer):
                    lcs_d2 = hypernyms_2[subnumer]
                lcs_dists.append(max([lcs_d1, lcs_d2]))
            h_dist = max(lcs_dists)
        else:
            h_dist = 0
    return ((math.exp(BETA * h_dist) - math.exp(-BETA * h_dist)) / 
        (math.exp(BETA * h_dist) + math.exp(-BETA * h_dist)))
    
def word_similarity(word_1, word_2):
    synset_pair = best_syn_pair(word_1, word_2)
    return (length_wise_distribution(synset_pair[0], synset_pair[1]) * 
        hierarchial_wise_distribution(synset_pair[0], synset_pair[1]))