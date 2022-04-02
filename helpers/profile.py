# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

def find_post(reddit, settings):
    for comment in reddit.redditor(settings['reddit']['username']).comments.new(limit=20):
        if comment.body in settings['phrases']['dones'] or comment.body in settings['phrases']['unclaims']:
            return None
        if comment.body in settings['phrases']['claims']:
            if comment.subreddit.name == 't5_3jqmx':
                return comment.submission
