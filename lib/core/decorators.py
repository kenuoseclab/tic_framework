#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   decorators.py
@Time    :   2020/06/19 22:06:01
@Author  :   - 
@Version :   1.0
@Contact :   huigou90@gmail.com
@License :   Apache License
@Desc    :   None
'''

# here put the import lib

import functools
import hashlib
import threading
from tic_framework.lib.core.datatype import LRUDict
from tic_framework.lib.core.settings import MAX_CACHE_ITEMS
from tic_framework.lib.core.settings import UNICODE_ENCODING
from tic_framework.lib.core.threads import getCurrentThreadData

_cache = {}
_cache_lock = threading.Lock()
_method_locks = {}

def cachedmethod(f):
    """
    Method with a cached content

    >>> __ = cachedmethod(lambda _: _)
    >>> __(1)
    1
    >>> __ = cachedmethod(lambda *args, **kwargs: args[0])
    >>> __(2)
    2
    >>> __ = cachedmethod(lambda *args, **kwargs: next(iter(kwargs.values())))
    >>> __(foobar=3)
    3
    
    Reference: http://code.activestate.com/recipes/325205-cache-decorator-in-python-24/
    """

    _cache[f] = LRUDict(capacity=MAX_CACHE_ITEMS)

    @functools.wraps(f)
    def _f(*args, **kwargs):
        key = int(hashlib.md5("|".join(str(_) for _ in (f, args, kwargs)).encode(UNICODE_ENCODING)).hexdigest(), 16) & 0x7fffffffffffffff

        try:
            with _cache_lock:
                result = _cache[f][key]
        except KeyError:
            result = f(*args, **kwargs)

            with _cache_lock:
                _cache[f][key] = result

        return result

    return _f