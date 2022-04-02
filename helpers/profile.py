# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

def find_post(reddit, settings):
    for comment in reddit.redditor(settings['reddit']['username']).comments.new(limit=20):
        if comment.body in settings['phrases']['dones']:
            return None
        if comment.body in settings['phrases']['claims']:
            if comment.subreddit.name.casefold() == 'transcribersofreddit' and \
                    comment.submission.author.name.casefold() == 'transcribersofreddit':
                return comment.submission
