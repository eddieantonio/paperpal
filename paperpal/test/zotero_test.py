#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

from ..zotero import Zotero, ZoteroError

def test_export_bibliography():
    z = Zotero()
    result = z.export_bibliography('PartyCrasher')

    assert '@inproceedings{alipour2013' in result

def test_list_papers():
    z = Zotero()
    result = z.list_papers('PartyCrasher')

    expected_item = dict(
        authors=[{'first': 'J.', 'last': 'Lerch'},
                 {'first': 'M.', 'last': 'Mezini'}],
        title='Finding Duplicates of Your Yet Unwritten Bug Report',
        cite_key='lerch2013',
        pdf_filename='/Users/eddieantonio/Library/Application Support/Zotero/Profiles/0648rls0.default/zotero/storage/IIVHABU8/Lerch y Mezini - 2013 - Finding Duplicates of Your Yet Unwritten Bug Repor.pdf'
    )

    assert len(result) >= 20
    assert expected_item in result
