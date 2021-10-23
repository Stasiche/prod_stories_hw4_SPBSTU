import json
import os
from typing import Tuple, List, Dict, Set
from time import sleep

from tqdm import tqdm

CURL_POST = 'curl -vvvv -X POST'
CURL_GET = 'curl -vvvv -X GET'


def upload(full_path: str, upload_url: str) -> Tuple[str, str]:
    r = json.loads(os.popen(f'{CURL_POST} -H "User-Id: test" --form file="@{full_path}" "{upload_url}"').read())
    uuid = r['uuid']
    filename = r['filename']
    return uuid, filename


def task(uuid: str, filename: str, task_url: str):
    config = {
        'uuid': uuid,
        'verison': '1',
        'file': filename,
        'id': 'test',
        'is_part': False
    }
    config = json.dumps(config)
    os.popen(f'{CURL_POST} -d \'{config}\' "{task_url}"').read()


def healthcheck(healthcheck_url: str) -> Tuple[str, str]:
    r = json.loads(os.popen(f'{CURL_GET} "{healthcheck_url}"').read())
    return r['status'], r['progress']


def get_bins_number_set(results_url: str) -> Set[int]:
    r = json.loads(os.popen(f'{CURL_GET} "{results_url}"').read())['histogram_data']
    return set([el['intervals'] for el in r if not el['type'].startswith('hull')])


def get_hists(bins_num: int, results_url: str) -> Dict[str, List[float]]:
    r = json.loads(os.popen(f'{CURL_GET} "{results_url}"').read())['histogram_data']
    hists = [el for el in r if (el['intervals'] == bins_num) and not el['type'].startswith('hull')]
    res = {}
    for el in hists:
        res[el['type']] = el['data']

    return res


def get_all_hists(results_url: str) -> Dict[int, Dict[str, List[float]]]:
    r = json.loads(os.popen(f'{CURL_GET} "{results_url}"').read())['histogram_data']
    res = {}
    for el in r:
        if not el['type'].startswith('hull'):
            res.setdefault(el['intervals'], {})[el['type']] = el['data']

    return res


def collect_hists(full_path: str, upload_url: str, task_url: str, healthcheck_url: str, results_url: str) -> \
        Dict[int, Dict[str, List[float]]]:
    uuid, filename = upload(full_path, upload_url)
    task(uuid, filename, task_url)

    pbar = tqdm(total=100)
    status, progress = healthcheck(healthcheck_url)
    while status != 'COMPLETED':
        status, progress = healthcheck(healthcheck_url)
        pbar.update(round(float(progress) - pbar.n))
        sleep(1)

    return get_all_hists(results_url)
