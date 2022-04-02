# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from time import sleep, time
from webbrowser import open as wbopen

import praw
import requests
from packaging import version
from praw.exceptions import MissingRequiredAttributeException
from pypresence import Presence
from tkinter.messagebox import askyesno

from helpers import *
from helpers.gvars import VERSION, TITLE_REGEX

def close_program(msg):
    print(msg)
    input('Press any key to exit...')
    exit()


if not assert_data():
    close_program('Data created, check the settings file please')

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

reddit = None
try:
    reddit = praw.Reddit(client_id=settings['reddit']['client_id'], client_secret=settings['reddit']['client_secret'],
                         user_agent="ToRPC v{} by /u/--B_L_A_N_K--".format(VERSION))
except MissingRequiredAttributeException as e:
    close_program('Missing required Reddit Authentication Attribute: ' + str(e))
if reddit is None:
    close_program('Failed Reddit auth')

rpc = Presence(settings['discord']['client_id'])
rpc.connect()
start_time = time()

while True:
    post = find_post(reddit, settings)
    if post is None:
        rpc_kwargs = {
            'details': settings['rpc_settings']['details'],
            'large_image': 'grafeaslogo',
            'small_image': 'idle',
            'small_text': 'Idling',
            'start': start_time,
            'buttons': [],
            'instance': False
        }
    else:
        r = handle_named_regex(TITLE_REGEX, post.title)
        if r is None:
            print("Error reading title: ", post.title)
            sleep(15)
            continue
        crosspost = reddit.submission(url=post.url)
        rpc_kwargs = {
            'details': settings['rpc_settings']['details'],
            'large_image': reddit.subreddit(r.group('subreddit')).icon_img,
            'large_text': r.group('subreddit'),
            'small_image': r.group('type').lower(),
            'small_text': r.group('type'),
            'start': start_time,
            'buttons': [],
            'instance': False
        }
        if not crosspost.over_18 and r.group('type') == 'Image':
            rpc_kwargs['small_image'] = rpc_kwargs['large_image']
            rpc_kwargs['small_text'] = rpc_kwargs['large_text']
            rpc_kwargs['large_image'] = crosspost.url
            rpc_kwargs['large_text'] = '"{}" by /u/{}'.format(crosspost.title, crosspost.author.name)
        if settings['rpc_settings']['show_post']:
            rpc_kwargs['state'] = 'Transcribing: "{}"'.format(r.group('title'))
        if settings['rpc_settings']['show_post_url']:
            rpc_kwargs['buttons'].append({'label': 'Go to Post', 'url': post.url})
    if settings['rpc_settings']['show_join']:
        rpc_kwargs['buttons'].append({'label': 'Join Us!',
                                      'url': 'https://www.reddit.com/r/TranscribersOfReddit/wiki/index'})
    rpc.update(**rpc_kwargs)
    sleep(15)
