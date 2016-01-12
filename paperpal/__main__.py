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

import sys
import os
import argparse
import shutil

from .k2pdfopt_wrapper import k2pdfopt
from .modification_time import modification_time
from .zotero import Zotero


def export_bibliograph(collection, destination):
    with open(filename, 'w') as output_file:
        output_file.write(Zotero().export_bibliography(collection))


def copy_pdfs(collection, directory):
    for source, destination in pdfs_to_update(collection, directory):
        shutil.copy(source, destination)


def to_ebook(collection, directory):
    pdfs = pdfs_to_update(collection, directory, with_info=True)
    for source, destination, info in pdfs:
        k2pdfopt(source,
                 destination,
                 title=info['title'],
                 author=authors_to_string(*info['authors']))


def author_to_string(author):
    """
    >>> author_to_string({'first': 'Devender'})
    'Devender'
    >>> author_to_string({'first': 'M. Night', 'last': 'Shamylaan'})
    'M. Night Shamylaan'
    """
    names = []
    if author.get('first', None):
        names.append(author['first'])
    if author.get('last', None):
        names.append(author['last'])

    return ' '.join(names)


def authors_to_string(*authors):
    """
    >>> author1 = {'first': 'S.', 'last': 'Miyamoto'}
    >>> author2 = {'first': 'K.', 'last': 'Kondo'}
    >>> author3 = {'first': 'H.', 'last': 'Tanaka'}
    >>> authors_to_string(author1)
    'S. Miyamoto'
    >>> authors_to_string(author1, author2)
    'S. Miyamoto and K. Kondo'
    >>> authors_to_string(author1, author2, author3)
    'S. Miyamoto, K. Kondo, H. Tanaka'
    """
    # Two authors: use " and "
    if len(authors) == 2:
        return (author_to_string(authors[0]) + ' and ' +
                author_to_string(authors[1]))

    # Use a comma separated list
    return ', '.join(author_to_string(auth) for auth in authors)


def pdfs_to_update(collection, destination_directory, with_info=False):
    pdfs = Zotero().list_papers(collection)

    destination = lambda *paths: os.path.join(destination_directory, *paths)

    for item in pdfs:
        cite_key = item['cite_key']
        pdf_path = item['pdf_filename']
        new_pdf = destination(cite_key + '.pdf')

        assert os.path.exists(pdf_path)
        if modification_time(pdf_path) > modification_time(new_pdf):
            if with_info:
                yield pdf_path, new_pdf, item
            else:
                yield pdf_path, new_pdf


def main(args=None):
    if args is None:
        args = sys.argv

    # TODO: Use argparse
    if len(args) != len(('paperpal', 'PaperPal', 'bibliography.bib')):
        sys.stderr.write('Usage:   %(name)s collection filename.bib\n'
                         % {'name': sys.argv[0]})
        exit(-1)

    _, collection, filename = sys.argv

    copy_pdfs(collection, filename)

if __name__ == '__main__':
    exit(main())
