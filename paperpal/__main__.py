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

import argparse
import os
import shutil
import sys
import warnings
import codecs

from paperpal import __version__ as version
from paperpal.k2pdfopt_wrapper import k2pdfopt
from paperpal.modification_time import modification_time
from paperpal.zotero import Zotero
from paperpal.fix_bibliography import fix_bibliography


parser = argparse.ArgumentParser(description="utilities for a streamlined "
                                             "bibliography workflow")
parser.add_argument('-v', '--version',
                    action='version',
                    version='%(prog)s ' + version)
subparsers = parser.add_subparsers(title='subcommands',
                                   description='valid subcommands',
                                   dest='command',
                                   help='')

# export options.
export_parser = subparsers.add_parser('export',
                                      help='exports a collection as a BibTeX '
                                           'bibliography')
export_parser.add_argument('collection',
                           help='name of the collection to export')
export_parser.add_argument('destination',
                           nargs='?',
                           default='bibliography.bib',
                           help='name of exported file '
                                '(default "bibliography.bib")')
export_parser.set_defaults(translator='bibtex')

translator_group = export_parser.add_mutually_exclusive_group()
translator_group.add_argument('--bibtex',
                              action='store_const', const='bibtex',
                              dest='translator',
                              help='use BibTeX as the translator '
                                   '(default)')
translator_group.add_argument('--biblatex',
                              action='store_const', const='biblatex',
                              dest='translator',
                              help='use BibLaTeX as the translator')
translator_group.add_argument('--better-bibtex',
                              action='store_const', const='better-bibtex',
                              dest='translator',
                              help='use Better BibTeX as the translator')
translator_group.add_argument('--better-biblatex',
                              action='store_const', const='better-biblatex',
                              dest='translator',
                              help='use Better BibLaTeX as the translator')

# copy options.
copy_parser = subparsers.add_parser('copy',
                                    help='copies PDFs from the collection '
                                         'to a directory')
copy_parser.add_argument('collection',
                         help='name of the collection')
copy_parser.add_argument('directory',
                         help='destination of copied PDFs')

# to-ebook options.
ebook_parser = subparsers.add_parser('to-ebook',
                                     help='copies PDFs from the collection '
                                          'to a directory')
ebook_parser.add_argument('collection',
                          help='name of the collection')
ebook_parser.add_argument('directory',
                          help='destination of translated PDFs')
ebook_parser.add_argument('args',
                          metavar='...',
                          nargs=argparse.REMAINDER,
                          help='remaining arguments are passed to k2pdfopt '
                               'unchanged')

# copy options.
fix_parser = subparsers.add_parser('fix-bibliography',
                                   help='Fixes an existing .bib file for '
                                   'easier usage with ieeetran.cls and '
                                   'sig-alternate.cls')
fix_parser.add_argument('bibliography',
                        help='name of input file')
fix_parser.add_argument('destination',
                        default='bibliography.bib',
                        help='name of exported file '
                        '(default "bibliography.bib")')


def export_bibliography(collection, destination, *args, **kwargs):
    with open(destination, 'w') as output_file:
        output_file.write(Zotero().export_bibliography(collection,
                                                       *args, **kwargs))


def copy_pdfs(collection, directory):
    for source, destination, _ in pdfs_to_update(collection, directory):
        shutil.copy(source, destination)


def to_ebook(collection, directory, *k2pdfopt_args):
    pdfs = pdfs_to_update(collection, directory)
    for source, destination, info in pdfs:
        k2pdfopt(source,
                 destination,
                 author=authors_to_string(*info['authors']),
                 title=info['title'],
                 *k2pdfopt_args)


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
    """
    Yields a tuple of PDFs that should be updated. The tuple is the original
    pdf, and the new PDF path. If with_info is requested,
    """
    pdfs = Zotero().list_papers(collection)

    def destination(*paths):
        return os.path.join(destination_directory, *paths)

    for item in pdfs:
        cite_key = item['cite_key']
        pdf_path = item['pdf_filename']

        if cite_key is None:
            warnings.warn('Please generate a cite key for '
                          '{author} "{title}" {year}'.format(**item))
            continue
        if pdf_path is None:
            warnings.warn('No PDF found for {cite_key}'.format(**item))
            continue

        new_pdf = destination(cite_key + '.pdf')
        if not os.path.exists(pdf_path):
            warnings.warn("I can't make sense of this path: "
                          '{!r}. Skipping...'.format(pdf_path))
            continue

        if modification_time(pdf_path) > modification_time(new_pdf):
            yield pdf_path, new_pdf, item


def fix_bibliography_wrapper(source, destination):
    with codecs.open(source, encoding="UTF-8") as bibtex_file:
        result = fix_bibliography(bibtex_file.read())

    with codecs.open(destination, encoding='UTF-8', mode='w') as output_file:
        output_file.write(result)


def main():
    options = parser.parse_args()

    if options.command == 'export':
        return export_bibliography(options.collection,
                                   options.destination,
                                   translator=options.translator)
    elif options.command == 'copy':
        return copy_pdfs(options.collection, options.directory)
    elif options.command == 'to-ebook':
        return to_ebook(options.collection, options.directory,
                        *options.args)
    elif options.command == 'fix-bibliography':
        return fix_bibliography_wrapper(options.bibliography,
                                        options.destination)


if __name__ == '__main__':
    exit(main())
