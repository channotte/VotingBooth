import hashlib

id = [['4_1', 0.046], ['8_1', 0.05], ['12_1', 0.054], ['16_1', 0.054], ['20_1', 0.048], ['4_2', 0.102], ['8_2', 0.109],
      ['12_2', 0.125], ['16_2', 0.117], ['20_2', 0.096], ['4_3', 0.178], ['8_3', 0.206], ['12_3', 0.235],
      ['16_3', 0.219],
      ['20_3', 0.175]]

id2 = [['4_1', 0.042], ['8_1', 0.05], ['12_1', 0.056], ['16_1', 0.052], ['20_1', 0.044], ['4_2', 0.096], ['8_2', 0.113],
       ['12_2', 0.127], ['16_2', 0.113], ['20_2', 0.09], ['4_3', 0.172], ['8_3', 0.217], ['12_3', 0.238],
       ['16_3', 0.213], ['20_3', 0.17]]


def code_hand_old(id):
    sorted_id = sorted(id)
    list_ratio = []
    counter = 0
    for index in range(0, len(sorted_id), 3):
        ratio1 = round(sorted_id[index][1] / sorted_id[index + 1][1], 3)
        print("num 1 ", sorted_id[index][1])
        print("denom 1", sorted_id[index + 1][1])
        ratio2 = round(sorted_id[index][1] / sorted_id[index + 2][1], 3)
        list_ratio.append([counter, ratio1, ratio2])
        counter += 1

    return list_ratio


# print(sorted(id))
# print(code_hand(id))
# print(code_hand(id2))

id_z1 = [['4_1', 0.048], ['8_1', 0.052], ['12_1', 0.063], ['16_1', 0.068], ['20_1', 0.059], ['4_2', 0.115],
         ['8_2', 0.111], ['12_2', 0.137], ['16_2', 0.142], ['20_2', 0.113], ['4_3', 0.191], ['8_3', 0.211],
         ['12_3', 0.242], ['16_3', 0.242], ['20_3', 0.196]]

id_z2 = [['4_1', 0.048], ['8_1', 0.05], ['12_1', 0.058], ['16_1', 0.064], ['20_1', 0.054], ['4_2', 0.113],
         ['8_2', 0.108],
         ['12_2', 0.13], ['16_2', 0.133], ['20_2', 0.107], ['4_3', 0.199], ['8_3', 0.21], ['12_3', 0.241],
         ['16_3', 0.239],
         ['20_3', 0.179]]

# print(code_hand(id_z1))
# print(code_hand(id_z2))
id_final = [[['Droite_0', 0.426, 0.213], ['Droite_1', 0.43, 0.22], ['Droite_2', 0.506, 0.106],
             ['Droite_3', 0.413, 0.216], ['Droite_4', 0.438, 0.222]],
            [['Gauche_0', 0.445, 0.24], ['Gauche_1', 0.461, 0.246], ['Gauche_2', 0.466, 0.26],
             ['Gauche_3', 0.462, 0.274], ['Gauche_4', 0.438, 0.232]]]
id_final_2 = [[['Gauche_0', 0.488, 0.276], ['Gauche_1', 0.46, 0.271], ['Gauche_2', 0.491, 0.267],
               ['Gauche_3', 0.437, 0.285], ['Gauche_4', 0.47, 0.252]],
              [['Droite_0', 0.461, 0.246], ['Droite_1', 0.47, 0.261], ['Droite_2', 0.491, 0.287],
               ['Droite_3', 0.456, 0.271], ['Droite_4', 0.462, 0.244]]]



list_id = [id_final, id_final_2]


def flatten(t):
    return [item for sublist in t for item in sublist]


def code_hand(id, ordre_main):
    dict_ratio_both = {}
    for id_hand, hand_identity in enumerate(id):
        main = ordre_main[id_hand]
        sorted_id = sorted(hand_identity)
        counter = 0
        for index in range(0, len(sorted_id), 3):
            ratio1 = round(sorted_id[index][1] / sorted_id[index + 1][1], 3)
            ratio2 = round(sorted_id[index][1] / sorted_id[index + 2][1], 3)
            dict_ratio_both[main + '_' + str(counter)] = [ratio1, ratio2]
            counter += 1

    return dict_ratio_both


# def mean(list_id):
#     liste_code_str = ['Droite_' + str(i) for i in range(0, 5)] + ['Gauche_' + str(i) for i in range(0, 5)]
#     for idx, item in enumerate(list_id):
#         if item[idx][0] in liste_code_str :
#


# coded = hashlib.sha256(str(id_final).encode())
# print("coded", coded.hexdigest())

double_id = [[['4_1', 0.04882517352190819], ['8_1', 0.051182310481747505], ['12_1', 0.05633673867912483],
              ['16_1', 0.06043686803070714], ['20_1', 0.047120307200764766], ['4_2', 0.11778781424250888],
              ['8_2', 0.11118053386771945], ['12_2', 0.1272369290383539], ['16_2', 0.12524390267094843],
              ['20_2', 0.09343842901804969], ['4_3', 0.18979569722211245], ['8_3', 0.20976590788569793],
              ['12_3', 0.2315875914206113], ['16_3', 0.21734731330452292], ['20_3', 0.17201067877056678]],
             [['4_1', 0.04903860883273505], ['8_1', 0.05217699910986748], ['12_1', 0.058416978720041465],
              ['16_1', 0.060919691129889285], ['20_1', 0.05287163848652698], ['4_2', 0.10909313880362861],
              ['8_2', 0.11319231422671772], ['12_2', 0.12925169412440124], ['16_2', 0.12824033596088677],
              ['20_2', 0.10875319280115156], ['4_3', 0.18377152297418117], ['8_3', 0.2129596998668084],
              ['12_3', 0.24174747212282857], ['16_3', 0.23173045060179534], ['20_3', 0.18666553315318044]]]

print(code_hand(double_id, ['Gauche', 'Droite']))

hand_dict = {'Gauche_0': [0.443, 0.243], 'Gauche_1': [0.483, 0.278], 'Gauche_2': [0.504, 0.274],
             'Gauche_3': [0.415, 0.257], 'Gauche_4': [0.46, 0.244], 'Droite_0': [0.452, 0.242],
             'Droite_1': [0.475, 0.263], 'Droite_2': [0.486, 0.283], 'Droite_3': [0.45, 0.267],
             'Droite_4': [0.461, 0.245]}


dict_1 = {'Droite_0': [0.426, 0.213], 'Droite_1': [0.43, 0.22], 'Droite_2': [0.506, 0.106],
          'Droite_3': [0.413, 0.216], 'Droite_4': [0.438, 0.222],
          'Gauche_0': [0.445, 0.24], 'Gauche_1': [0.461, 0.246], 'Gauche_2': [0.466, 0.26],
          'Gauche_3': [0.462, 0.274], 'Gauche_4': [0.438, 0.232]}

list_of_dict = [dict_1, hand_dict]

import pandas as pd


def aggregate_dicts(dicts, operation=lambda x: sum(x) / len(x)):
    """
    Aggregate a sequence of dictionaries to a single dictionary using `operation`. `Operation` should
    reduce a list of all values with the same key. Keyrs that are not found in one dictionary will
    be mapped to `None`, `operation` can then chose how to deal with those.
    """
    all_keys = set().union(*[el.keys() for el in dicts])
    return {k: operation([dic.get(k, None) for dic in dicts]) for k in all_keys}


def mean_no_none(l):
    l_no_none_x = [el[0] for el in l if el is not None]
    print(l_no_none_x)
    l_no_none_y = [el[1] for el in l if el is not None]
    print(l_no_none_y)

    return [sum(l_no_none_x) / len(l_no_none_x),sum(l_no_none_y) / len(l_no_none_y)]


print("agg", aggregate_dicts(list_of_dict, operation=mean_no_none))

# print("moy",df.mean())
# answer = dict(df.mean())
# print("reponse", answer)
