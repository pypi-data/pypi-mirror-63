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

# Import from pygit2
from .ffi import ffi


def to_bytes(s, encoding='utf-8', errors='strict'):
    if s == ffi.NULL or s is None:
        return ffi.NULL

    if isinstance(s, bytes):
        return s

    return s.encode(encoding, errors)


def to_str(s):
    if type(s) is str:
        return s

    if type(s) is bytes:
        return s.decode()

    raise TypeError('unexpected type "%s"' % repr(s))


def strarray_to_strings(arr):
    l = [None] * arr.count
    for i in range(arr.count):
        l[i] = ffi.string(arr.strings[i]).decode('utf-8')

    return l


class StrArray(object):
    """A git_strarray wrapper

    Use this in order to get a git_strarray* to pass to libgit2 out of a
    list of strings. This has a context manager, which you should use, e.g.

        with StrArray(list_of_strings) as arr:
            C.git_function_that_takes_strarray(arr)
    """

    def __init__(self, l):
        # Allow passing in None as lg2 typically considers them the same as empty
        if l is None:
            self.array = ffi.NULL
            return

        if not isinstance(l, list):
            raise TypeError("Value must be a list")

        strings = [None] * len(l)
        for i in range(len(l)):
            if not isinstance(l[i], str):
                raise TypeError("Value must be a string")

            strings[i] = ffi.new('char []', to_bytes(l[i]))

        self._arr = ffi.new('char *[]', strings)
        self._strings = strings
        self.array = ffi.new('git_strarray *', [self._arr, len(strings)])

    def __enter__(self):
        return self.array

    def __exit__(self, type, value, traceback):
        pass


class GenericIterator(object):
    """Helper to easily implement an iterator.

    The constructor gets a container which must implement __len__ and
    __getitem__
    """

    def __init__(self, container):
        self.container = container
        self.length = len(container)
        self.idx = 0

    def next(self):
        return self.__next__()

    def __next__(self):
        idx = self.idx
        if idx >= self.length:
            raise StopIteration

        self.idx += 1
        return self.container[idx]
