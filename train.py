import argparse
import json
import numpy as np
from gensim.models import word2vec

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str, default='log.json')
    parser.add_argument('--model', '-m', type=str, default='model.vec')
    args = parser.parse_args()

    input_filename = args.input
    model_filename = args.model

    with open(input_filename, 'r') as f:
        data = json.load(f)
    
    sentence_list = []
    channel_ids=[d['id'] for d in data['channels']]
    
    for channel_id in channel_ids:
        if channel_id in data['messages']:
            messages = list(data['messages'][channel_id])
            messages = list(filter(lambda x: 'parent_user_id' not in x, messages))
            messages = list(filter(lambda x: 'subtype' not in x or x['subtype'] != 'bot_message', messages))
    
            sentence = []
            for m in messages:
                if not m.get('user'):
                    continue
                sentence.append(m['user'])
            sentence_list.append(sentence)
    
            for m in messages:
                if 'replies' in m:
                    sentence = [r['user'] for r in m['replies']]
                    if len(sentence) > 3:
                        sentence_list.append(sentence)
    
    model = word2vec.Word2Vec(sentence_list, size=32, min_count=5, window=5, iter=300)
    
    model.save(model_filename)
