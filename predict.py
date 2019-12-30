import json
import argparse
import numpy as np
from sklearn import linear_model
from gensim.models import word2vec
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
    vec_list = util.create_vec_list(model, name_list, name2id)
    
    menber_dict = np.array(vec_list).T
    
    target_idx = name_list.index(target_name)
    target_vec = model.wv.word_vec(name2id[target_name])
    
    # 対象者のベクトルを辞書から削除
    idx = list(range(0,target_idx)) + list(range(target_idx+1,len(name_list)))
    tmp_menber_dict = menber_dict[:,idx]
    tmp_name_list = np.array(name_list)[idx]
    
    clf = linear_model.Lasso(alpha=0.9)
    clf.fit(tmp_menber_dict, target_vec)
    
    selected_idx = np.where(np.array(clf.coef_) != 0)[0]
    selected_names = tmp_name_list[selected_idx]
    selected_coef = clf.coef_[selected_idx]
    
    for n, c in zip(selected_names, selected_coef):
        print('{}: {}'.format(n, c))
