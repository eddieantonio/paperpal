#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import bibtexparser

from ..fix_bibliography import fix_bibliography


bad_bib = ur"""
@inproceedings{vasic2009,
  location = {{New York, NY, USA}},
  title = {Making {{Cluster Applications Energy}}-aware},
  isbn = {978-1-60558-585-7},
  url = {http://doi.acm.org/10.1145/1555271.1555281},
  doi = {10.1145/1555271.1555281},
  abstract = {Power consumption has become a critical issue in large scale clusters. Existing solutions for addressing the servers' energy consumption suggest "shrinking" the set of active machines, at least until the more power-proportional hardware devices become available. This paper demonstrates that leveraging the sleeping state, however, may lead to unacceptably poor performance and low data availability if the distributed services are not aware of the power management's actions. Therefore, we present an architecture for cluster services in which the deployed services overcome this problem by actively participating in any action taken by the power management. We propose, implement, and evaluate modifications for the Hadoop Distributed File System and the MapReduce clone that make them capable of operating efficiently under limited power budgets.},
  timestamp = {2016-05-20T05:50:14Z},
  booktitle = {Proceedings of the 1st {{Workshop}} on {{Automated Control}} for {{Datacenters}} and {{Clouds}}},
  series = {ACDC '09},
  publisher = {{ACM}},
  author = {Vasić, Nedeljko and Barisits, Martin and Salzgeber, Vincent and Kostic, Dejan},
  urldate = {2016-05-20},
  date = {2009},
  pages = {37--42},
  keywords = {cluster applications,cluster services,energy-awareness,storage}
}
"""

def test_fix_bibiliography():
    result = fix_bibliography(bad_bib)

    assert all(ord(char) < 0x80 for char in result), "Not ASCII"

    # Now parse it:
    bibtex = bibtexparser.loads(result)

    entry = bibtex.entries[0]

    assert entry['author'].startswith(r"Vasi{\' c}"), "Did not handle Unicode escape"
    assert 'url' not in entry, "Did not delete URL"
    assert 'year' in entry and entry['year'] == '2009', "Did not handle year"
