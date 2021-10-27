import pandas as pd
import json
from typing import Dict, List
from tqdm import tqdm
from itertools import product
import os
from os.path import join

def get_hists(hists_path: str, hist_type: str, n_bins: int) -> Dict[str, List[float]]:
    res = {}
    for name in [el for el in os.listdir(hists_path) if el.endswith('.json')]:
        with open(join(hists_path, name), 'rb') as f:
            data = json.loads(f.read())['histogram_data']
            res[name] = [el for el in data if (el['type']==hist_type) and (el['intervals']==n_bins)][0]['data']
        
    return res

def convert_jsons_to_csv(hists_path: str, labels_path: str) -> pd.DataFrame:
    hists_types = ['model_bounding_sphere_concentric_sphere',
              'model_bounding_sphere_missed',
              'model_bounding_sphere_strict_outer',
              'model_bounding_sphere_strict_outer_absolute']

    ns_bins = [8, 16, 32, 64, 128]
    
    
    dataset = {'model_name' : [], 'hist_type': [], 'n_bins': [], 'values': []}
    for hist_type, n_bins in tqdm(product(hists_types, ns_bins), total=len(list(product(hists_types, ns_bins)))):
        for model_name, vals in get_hists(hists_path, hist_type, n_bins).items():
            dataset['hist_type'].append(hist_type)
            dataset['n_bins'].append(n_bins)
            dataset['model_name'].append(model_name.split('.')[0])
            dataset['values'].append(vals)
    
    labels = pd.read_csv(labels_path)
    labels.type = labels.type.apply(lambda x: x.split('.')[0])

    dataset_labels = pd.merge(labels, pd.DataFrame(dataset), left_on='model', right_on='model_name')
    return dataset_labels