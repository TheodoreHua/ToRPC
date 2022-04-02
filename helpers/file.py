# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from os import mkdir
from os.path import isfile, isdir
from typing import Union

import yaml

default_settings = {
    'reddit': {
        'client_id': '',
        'client_secret': ''
    },
    'discord': {
        'client_id': ''
    },
    'rpc_settings': {
        'show_post': True,
        'show_post_url': True,
        'show_join': True
    },
    'update_check': True
}

def check_dict(d: dict, expected: dict, fixed_dict=None) -> Union[bool, dict]:
    """Goes through each dict and subdict to check if the keys in expected are in d, if not, they're filled in with the
    value in expected

    :param d: Dict to check
    :param expected: Dict with expected keys
    :param fixed_dict: Patched version of d
    :return: True if check succeeded, list of missing keys if check failed
    """
    if d is None:
        d = {}  # Set d to an empty dict if d is None, which happens when YAML file is empty
    if fixed_dict is None:
        fixed_dict = d.copy()  # Set fixed dict to be a copy of d if not provided in args
    else:
        fixed_dict = fixed_dict.copy()  # Set fixed dict to be a copy of one provided in args if given

    for k, v in expected.items():
        if k not in d.keys():
            fixed_dict[k] = expected[k]
        if isinstance(v, dict):
            sr = check_dict(d.get(k, {}), expected[k], fixed_dict[k])
            if isinstance(sr, dict):
                fixed_dict[k] = sr

    return True if fixed_dict == d else {k: fixed_dict[k] for k in expected}  # Hacky way to sort & remove unused keys

def assert_data() -> bool:
    if not isdir('data'):
        mkdir('data')
    if not isfile('data/settings.yaml'):
        with open('data/settings.yaml', 'w') as f:
            f.write(yaml.dump(default_settings, sort_keys=False))
        return False
    else:
        r = check_dict(load_settings(), default_settings)
        if isinstance(r, dict):
            with open('data/settings.yaml', 'w') as f:
                f.write(yaml.dump(r, sort_keys=False))
            return False
    return True

def load_settings() -> dict:
    with open('data/settings.yaml', 'r') as f:
        return yaml.load(f.read(), Loader=yaml.FullLoader)
