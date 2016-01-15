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

import subprocess

__all__ = ['k2pdfopt']


def k2pdfopt(filename, destination, *extra_args, **kwargs):
    args = ['k2pdfopt',
            '-ui-', '-x',
            '-mode', '2col',
            '-dev', 'kpw']

    if 'author' in kwargs:
        args += ['-author', kwargs['author']]
    if 'title' in kwargs:
        args += ['-title', kwargs['title']]

    args += extra_args
    args += ['-o', destination, filename]

    return subprocess.call(args)
