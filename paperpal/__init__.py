#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

# Copyright 2016 Eddie Antonio Santos <easantos@ualberta.ca>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
pal for zotero paper management.
"""

import argparse
import json
import logging
import os
import sys
import tempfile

import mozrepl

NEGATIVE_INFINITY = -float('inf')
logging.basicConfig(level=logging.DEBUG)

__version__ = '0.1.0'

def resource_path(*args):
    return os.path.join(os.path.dirname(__file__), *args)

with open(resource_path('zotero-bridge.js')) as javascript_file:
    JS_RUNTIME = javascript_file.read()

class ZoteroError(Exception):
    def __init__(self, reason):
        super(ZoteroError, self).__init__(repr(reason))
        self.reason = reason

class Zotero(object):
    def __init__(self):
        self.repl = mozrepl.Mozrepl()

    def copy_pdfs(self, collection, destination):
        pass

    def convert_pdfs(self, collection, destination):
        pass

    def export_bibliography(self, collection):
        with tempfile.NamedTemporaryFile() as temporary:
            self._send_to_repl('exportBibliography',
                               filename=temporary.name,
                               collection=collection)
            # Return the contents.
            temporary.seek(0)
            return temporary.read()

    def _send_to_repl(self, action, **options):
        # INTENTIONALLY inject code into the code snippet.
        code = JS_RUNTIME % {
                'action': repr(action),
                'options': json.dumps(options),
                'open_comment': '/*',
                'close_comment': '*/'
        }
        logging.debug(code)

        status, payload = tuple(self.repl.execute(code))
        if status == 'error':
            raise ZoteroError(payload)

        return payload

def modification_time(filename):
    """
    Returns modification time of the given filename.
    Returns negative infinity if the file does not exist.
    """
    if not os.path.exists(filename):
        return NEGATIVE_INFINITY
    return os.stat(filename).st_mtime

def main(args=None):
    if args is None:
        args = sys.argv

    # TODO: Use argparse
    if len(args) != len(('paperpal', 'PaperPal', 'bibliography.bib')):
        sys.stderr.write('Usage:   %(name)s collection filename.bib\n'
                         % {'name': sys.argv[0]})
        exit(-1)

    _, collection, filename = sys.argv

    with open(filename, 'w') as output_file:
        output_file.write(Zotero().export_bibliography(collection))

if __name__ == '__main__':
    exit(main())
