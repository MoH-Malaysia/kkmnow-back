import pandas as pd
import json
import numpy as np
import copy
import ast
from mergedeep import merge
import re

'''
State abbreviations,
to use for each chart / dashboard
'''
STATE_ABBR = {'Johor': 'jhr',
              'Kedah': 'kdh',
              'Kelantan': 'ktn',
              'Klang Valley': 'kvy',
              'Melaka': 'mlk',
              'Negeri Sembilan': 'nsn',
              'Pahang': 'phg',
              'Perak': 'prk',
              'Perlis': 'pls',
              'Pulau Pinang': 'png',
              'Sabah': 'sbh',
              'Sarawak': 'swk',
              'Selangor': 'sgr',
              'Terengganu': 'trg',
              'W.P. Labuan': 'lbn',
              'W.P. Putrajaya': 'pjy',
              'W.P. Kuala Lumpur': 'kul',
              'Malaysia': 'mys'
            }

'''
Gets all nested keys,
within a dictionary
'''
def get_nested_keys(d, keys, search):
    for k, v in d.items():
        if isinstance(v, dict):
            get_nested_keys(v, keys, search)
            if search == 'KEYS' :
                keys.append(k)
        else :
            if search == 'VALUES' :
                if len(keys) == 0 :
                    keys.append(dict({k : v}))
                else :
                    keys[0][k] = v

'''
Gets a value of a dictionary,
based on the nested keys
'''
def get_dict(d, keys):
    for key in keys:
        d = d[key]
    return d

'''
Sets a dictionary,
based on the nested keys
'''
def set_dict(d, keys, value, operation):
    d = get_dict(d, keys[:-1])
    if (operation == "APPEND") and (d[keys[-1]] != {}) :
        d[keys[-1]]['data'].append(value['data'][0])
    elif operation  == "BARCHART" :
        d[keys[-1]].append(value)
    else : 
        d[keys[-1]] = value

'''
Converts parquet files into csv
'''
def convert_pq_to_csv(read_dir, export_dir, file_list) :
    for f in file_list :
        df = pd.read_parquet(read_dir + f + '.parquet')
        df.to_csv(export_dir + f + ".csv")

'''
Prints a json page,
from dict to json
'''
def print_page(filename, dict) : 
    with open(filename, 'w') as json_file:
        json.dump(dict, json_file)

'''
Custom renaming,
for labels within a chart
'''
def rename_labels(label, rname_dict) : 
    txt = label

    for k, v in rname_dict.items() :
        txt = re.sub(k, v, txt)
        # txt = txt.replace(k, v)

    return txt.replace("_", " ").title()

'''
Prepopulates a dictionary,
with the respective keys
'''
def prepopulate_dict(keys, df) :
    res = {}

    for i in keys[::-1] :
        temp = {}
        for x in df[i].unique().tolist() :
            temp[x] = {}
        res[i] = temp

    count = 0
    prev = {}
    for k, v in res.items() :          
        for i, x in v.items() :
            if count > 0 :
                v[i].update(prev)
        prev = v
        count = count + 1

    return res[keys[0]]
