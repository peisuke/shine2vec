import argparse
import json
import numpy as np
from gensim.models import word2vec
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import util

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str, default='log.json')
    parser.add_argument('--model', '-m', type=str, default='model.vec')
    args = parser.parse_args()

    input_filename = args.input
    model_filename = args.model

    with open(input_filename, 'r') as f:
        data = json.load(f)
    
    model = word2vec.Word2Vec.load(model_filename)
    
    id2name, name2id = util.create_dict(data)
    name_list = util.create_name_list(model, id2name)
    vec_list = util.create_vec_list(model, name_list, name2id)
    
    ret = TSNE(n_components=2, random_state=0).fit_transform(vec_list)
    
    plt.figure(figsize=(16, 16))
    for r, n in zip(ret, name_list):
        plt.scatter(r[0], r[1], color='r')
        plt.text(r[0]+0.3, r[1]+0.3, n, fontsize=9)
    
    plt.show()
