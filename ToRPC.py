# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from time import sleep
from webbrowser import open as wbopen

import praw
import requests
from packaging import version
from praw.exceptions import MissingRequiredAttributeException
from pypresence import Presence
from tkinter.messagebox import askyesno

from helpers import *
from helpers.gvars import *

assert_data()
settings = load_settings()

if settings['update_check']:
    # Check GitHub API endpoint
    resp = requests.get("https://api.github.com/repos/TheodoreHua/ToRPC/releases/latest")
    # Check whether response is a success
    if resp.status_code == 200:
        resp_js = resp.json()
        # Check whether the version number of remote is greater than version number of local (to avoid dev conflict)
        if version.parse(resp_js["tag_name"]) > version.parse(VERSION):
            # Ask user whether they want to open the releases page
            yn_resp = askyesno("New Version",
                               "A new version ({}) is available.\n\nPress yes to open page and no to ignore.\nUpdate "
                               "checking can be disabled in config.".format(resp_js["tag_name"]))
            if yn_resp:
                wbopen("https://github.com/TheodoreHua/ToRPC/releases/latest")

try:
    reddit = praw.Reddit(client_id=settings['reddit']['client_id'], client_secret=settings['reddit']['client_secret'],
                         user_agent="ToRPC v{} by /u/--B_L_A_N_K--".format(VERSION))
except MissingRequiredAttributeException as e:
    print('Missing required Reddit Authentication Attribute:', str(e))
    exit()
