from argparse import ArgumentParser
import os
import pickle
from tqdm import tqdm

try:
    from utils import collect_hists
except ModuleNotFoundError:
    from src.utils import collect_hists

API_URL = 'http://45.14.48.80:10000/'
UPLOAD_URL = API_URL + 'upload'
TASK_URL = API_URL + 'task'
HEALTHCHECK_URL = API_URL + 'healthcheck'
RESULTS_URL = API_URL + 'results'


def main(models_path: str, dataset_name: str):
    models_lst = [el for el in os.listdir(models_path) if el.endswith('.stl')]

    dataset = {}
    for model_name in tqdm(models_lst):
        full_path = f'{models_path}/{model_name}'
        dataset[model_name] = collect_hists(full_path, UPLOAD_URL, TASK_URL, HEALTHCHECK_URL, RESULTS_URL)

    with open(f'{dataset_name}.pkl', 'wb') as f:
        pickle.dump(dataset, f)


if __name__ == "__main__":
    cwd = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    __arg_parser = ArgumentParser()
    __arg_parser.add_argument('--models', type=str, default=f'{cwd}/data/models',
                              help='Path to directory with stl models')
    __arg_parser.add_argument('--dataset', type=str, default='dataset', help='Dataset pickle file name')

    __args = __arg_parser.parse_args()
    main(__args.models, __args.dataset)
