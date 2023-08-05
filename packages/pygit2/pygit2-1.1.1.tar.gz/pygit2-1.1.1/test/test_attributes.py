# Copyright 2010-2020 The pygit2 contributors
#
# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2,
# as published by the Free Software Foundation.
#
# In addition to the permissions in the GNU General Public License,
# the authors give you unlimited permission to link the compiled
# version of this file into combinations with other programs,
# and to distribute those combinations without any restriction
# coming from the use of this file.  (The General Public License
# restrictions do apply in other respects; for example, they cover
# modification of the file, and distribution when not linked into
# a combined executable.)
#
# This file is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301, USA.

# Standard Library
from os.path import join

# pygit2
from . import utils

try:
    import __pypy__
except ImportError:
    __pypy__ = None


class RepositorySignatureTest(utils.RepoTestCase):

    def test_no_attr(self):
        assert self.repo.get_attr('file', 'foo') is None

        with open(join(self.repo.workdir, '.gitattributes'), 'w+') as f:
            print('*.py  text\n', file=f)
            print('*.jpg -text\n', file=f)
            print('*.sh  eol=lf\n', file=f)

        assert self.repo.get_attr('file.py', 'foo') is None
        assert self.repo.get_attr('file.py', 'text')
        assert not self.repo.get_attr('file.jpg', 'text')
        assert "lf" == self.repo.get_attr('file.sh', 'eol')
