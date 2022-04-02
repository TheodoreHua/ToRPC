# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from .file import assert_data, load_settings
from .profile import find_post

def handle_named_regex(regex, search_string):
    try:
        return next(regex.finditer(search_string))
    except StopIteration:
        return None
