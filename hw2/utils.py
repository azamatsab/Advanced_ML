import numpy as np


def get_ids_by_date(years, tournaments, results):
    ids = []
    for id_ in tournaments:
        if id_ == 6149:    # all masks is 0 in this tournament
            continue
        tournament = tournaments[id_]
        date_start = int(tournament['dateStart'][:4])
        if date_start in years:
            flag = True
            if len(results[id_]):
                mask_len = None
                for i in range(len(results[id_])):
                    if 'mask' not in results[id_][i] or results[id_][i]['mask'] is None:
                        flag = False
                        continue
                    if mask_len is None:
                        mask_len = len(results[id_][i]['mask'])
                    elif mask_len != len(results[id_][i]['mask']):
                        flag = False
                if flag:
                    ids.append(id_)
    return ids

def get_top(x, topk):
    out = [(k, v) for k, v in sorted(x.items(), key=lambda item: np.mean(item[1]), reverse=True)]
    return out[:topk]

def get_top_players(x, topk, players, player_appereances):
    top_players = get_top(x, topk)
    info = []
    for player, score in top_players:
        info.append((players[player]['name'] + ' ' + players[player]['surname'], score, player_appereances[player]))
    return info

def get_top_comps(x, topk, tournaments):
    top_comps = get_top(x, topk)
    info = []
    for cmp, score in top_comps:
        info.append((tournaments[cmp]['name'], score))
    return info

def create_nested_dict(train_ids, results, player_p=None, z_s=False):
    nested_dict = {}
    for comp in train_ids:
        nested_dict[comp] = {}
        for team in results[comp]:
            team_id = team['team']['id']
            nested_dict[comp][team_id] = {}
            members = team['teamMembers']
            for member in members:
                player_id = member['player']['id']
                if not z_s:
                    if player_p is None:
                        nested_dict[comp][team_id][player_id] = np.random.uniform(0, 1)
                    else:
                        nested_dict[comp][team_id][player_id] = player_p[player_id]
                else:
                    nested_dict[comp][team_id][player_id] = []
    return nested_dict

def create_players_dict(train_ids, results, scalar=False):
    simple_dict = {}
    for comp in train_ids:
        for team in results[comp]:
            members = team['teamMembers']
            for member in members:
                player_id = member['player']['id']
                if scalar:
                    simple_dict[player_id] = np.random.uniform(1, 2)
                else:
                    simple_dict[player_id] = []
    return simple_dict

def to_int(mask):
    return np.array([int(m) for m in mask if m in ['0', '1']])

def get_players_appereances(train_ids, results):
    simple_dict = {}
    for comp in train_ids:
        for team in results[comp]:
            members = team['teamMembers']
            mask = team['mask']
            mask = to_int(mask)
            value = mask.shape[0]
            for member in members:
                player_id = member['player']['id']
                if player_id in simple_dict:
                    simple_dict[player_id] += value
                else:
                    simple_dict[player_id] = value
    return simple_dict

def generate_players_p(train_ids, results):
    simple_dict = {}
    for comp in train_ids:
        for team in results[comp]:
            members = team['teamMembers']
            for member in members:
                player_id = member['player']['id']
                simple_dict[player_id] = np.random.uniform(0, 1)
    return simple_dict
