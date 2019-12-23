def create_dict(data):
    id2name = {d['id']: d['profile']['display_name'] for d in data['users']}
    name2id = {d['profile']['display_name']: d['id'] for d in data['users']}
    return id2name, name2id

def create_name_list(model, id2name):
    user_ids = list(model.wv.vocab.keys())
    name_list = [id2name[id] for id in user_ids if id in id2name]
    return name_list

def create_vec_list(model, name_list, name2id):
    vec_list = []
    for name in name_list:
        v = model.wv.word_vec(name2id[name])
        vec_list.append(v)
    return vec_list
