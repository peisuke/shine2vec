def create_dict(data):
    id2name = {d['id']: d['profile']['display_name'] for d in data['users']}
    name2id = {d['profile']['display_name']: d['id'] for d in data['users']}
    return id2name, name2id

def create_name_list(model, id2name):
    #user_ids = list(model.wv.vocab.keys())
    user_ids = model.wv.index_to_key
    name_list = [id2name[id] for id in user_ids if id in id2name]
    return name_list

def create_vec_list(model, name_list, name2id):
    vec_list = []
    new_name_list = []
    for name in name_list:
        id = name2id[name]
        if id in model.wv.key_to_index:
            v = model.wv.word_vec(id)
            vec_list.append(v)
            new_name_list.append(name)
    return new_name_list, vec_list
