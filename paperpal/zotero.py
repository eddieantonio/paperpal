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

import json
import logging
import tempfile
import urllib

import mozrepl

from .resource_path import resource_path


with open(resource_path('zotero-bridge.js')) as javascript_file:
    JS_RUNTIME = javascript_file.read()

NAME_TO_TRANSLATOR_ID = {
    'bibtex':           '9cb70025-a888-4a29-a210-93ec52da40d4',
    'biblatex':         'b6e39b57-8942-4d11-8259-342c46ce395f',
    'better-bibtex':    'f895aa0d-f28e-47fe-b247-2ea77c6ed583',
    'better-biblatex':  'f895aa0d-f28e-47fe-b247-2ea77c6ed583'

}


class ZoteroError(Exception):
    def __init__(self, reason):
        super(ZoteroError, self).__init__(repr(reason))
        self.reason = reason


class Zotero(object):
    def __init__(self):
        self.repl = mozrepl.Mozrepl()

    def list_papers(self, collection):
        result = self._send_to_repl('list', collection=collection)
        return [fix_filename(item) for item in result]

    def export_bibliography(self, collection, translator=None):
        if translator is not None:
            translator = NAME_TO_TRANSLATOR_ID[translator]

        with tempfile.NamedTemporaryFile() as temporary:
            self._send_to_repl('exportBibliography',
                               filename=temporary.name,
                               collection=collection,
                               translator=translator)
            # Return the contents.
            temporary.seek(0)
            return temporary.read()

    def _send_to_repl(self, action, **options):
        # INTENTIONALLY inject code into the code snippet.
        code = JS_RUNTIME % {
            'action': json.dumps(action),
            'options': json.dumps(options),
            'open_comment': '/*',
            'close_comment': '*/'
        }

        result = self.repl.execute(code)
        status, json_payload = tuple(result)
        payload = json.loads(json_payload)

        if status == 'error':
            raise ZoteroError(payload)

        return payload


def fix_filename(item):
    """
    >>> datum = {'pdf_filename': 'file:///Users/Foo%20Bar/herp.pdf'}
    >>> fix_filename(datum)['pdf_filename']
    '/Users/Foo Bar/herp.pdf'
    """
    if item['pdf_filename'] is None:
        return item

    original = item['pdf_filename']
    if original.startswith('file://'):
        original = original[len('file://'):]
    filename = urllib.unquote(original)
    item.update(pdf_filename=filename)

    return item
