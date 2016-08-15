#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re

import bibtexparser

from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import homogeneize_latex_encoding


__all__ = ['fix_bibliography']


def fix_bibliography(bibtex_string):
    """
    Given a bibliography file, `fixes` it by removing URLs from articles,
    ASCIIifying all the fields and replacing dates with years.
    """

    # Make a parser that will ASCIIify everything:
    # See: https://bibtexparser.readthedocs.io/en/v0.6.2/tutorial.html#accents-and-weird-characters
    parser = BibTexParser()
    parser.customization = homogeneize_latex_encoding

    bibtex = bibtexparser.loads(bibtex_string, parser=parser)

    for entry in bibtex.entries:
        fix_entry(entry)

    return bibtexparser.dumps(bibtex)


def fix_entry(entry):
    # Add the year from the date.
    if 'date' in entry:
        entry['year'] = str(parse_year(entry['date']))

    # In most entry types, get rid of the URL.
    if entry['ENTRYTYPE'] not in ('online', 'misc') and 'url' in entry:
        del entry['url']

    # Get rid of the DOI.
    if 'doi' in entry:
        del entry['doi']


def parse_year(string):
    """
    >>> parse_year('2013')
    2013
    >>> parse_year('April 2014')
    2014
    >>> parse_year('06/2012')
    2012
    """

    match = re.search('\d{4}', string)
    if not match:
        raise ValueError('Could not parse year in ' + repr(string))

    return int(match.group(0))
