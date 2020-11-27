import argparse
import json
import numpy as np
from sklearn import linear_model
from gensim.models import word2vec

from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

import util

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str, default='log.json')
    parser.add_argument('--model', '-m', type=str, default='model.vec')
    parser.add_argument('--target', '-t', type=str, required=True)
    args = parser.parse_args()
    
    input_filename = args.input
    model_filename = args.model
    target_name = args.target

    with open(input_filename, 'r') as f:
        data = json.load(f)
    
    model = word2vec.Word2Vec.load(model_filename)
    
    id2name, name2id = util.create_dict(data)
    name_list = util.create_name_list(model, id2name)
    
    ret = model.wv.most_similar(positive=[name2id[target_name]]) 
    
    for r in ret:
        if r[0] in id2name:
            print(id2name[r[0]], r[1])
