#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   convert.py
@Time    :   2020/06/19 17:55:43
@Author  :   - 
@Version :   1.0
@Contact :   huigou90@gmail.com
@License :   Apache License
@Desc    :   None
'''

# here put the import lib
import sys
import base64
import binascii
import codecs
import collections
from tic_framework.lib.core.data import conf
from tic_framework.lib.core.data import kb
from tic_framework.thirdparty import six
from tic_framework.thirdparty.six import unichr as _unichr
from tic_framework.lib.core.settings import IS_WIN, IS_TTY, UNICODE_ENCODING


def getUnicode(value, encoding=None, noneToNull=False):
    """
    Returns the unicode representation of the supplied value

    >>> getUnicode('test') == u'test'
    True
    >>> getUnicode(1) == u'1'
    True
    """

    if noneToNull and value is None:
        return NULL

    if isinstance(value, six.text_type):
        return value
    elif isinstance(value, six.binary_type):
        # Heuristics (if encoding not explicitly specified)
        candidates = filterNone((encoding, kb.get("pageEncoding") if kb.get("originalPage") else None, conf.get("encoding"), UNICODE_ENCODING, sys.getfilesystemencoding()))
        if all(_ in value for _ in (b'<', b'>')):
            pass
        elif any(_ in value for _ in (b":\\", b'/', b'.')) and b'\n' not in value:
            candidates = filterNone((encoding, sys.getfilesystemencoding(), kb.get("pageEncoding") if kb.get("originalPage") else None, UNICODE_ENCODING, conf.get("encoding")))
        elif conf.get("encoding") and b'\n' not in value:
            candidates = filterNone((encoding, conf.get("encoding"), kb.get("pageEncoding") if kb.get("originalPage") else None, sys.getfilesystemencoding(), UNICODE_ENCODING))

        for candidate in candidates:
            try:
                return six.text_type(value, candidate)
            except (UnicodeDecodeError, LookupError):
                pass
        
        try:
            return six.text_type(value, encoding or (kb.get("pageEncoding") if kb.get("originalPage") else None) or UNICODE_ENCODING)
        except UnicodeDecodeError:
            return six.text_type(value, UNICODE_ENCODING, errors="reversible")
    elif isListLike(value):
        value = list(getUnicode(_, encoding, noneToNull) for _ in value)
        return value
    else:
        try:
            return six.text_type(value)
        except UnicodeDecodeError:
            return six.text_type(str(value), errors="ignore")  # encoding ignored for non-basestring instances

def filterNone(values):  # Cross-referenced function
    return [_ for _ in values if _] if isinstance(values, collections.Iterable) else values


def stdoutEncode(value):
    """
    Returns binary representation of a given Unicode value safe for writing to stdout
    """

    value = value or ""

    if IS_WIN and IS_TTY and kb.get("codePage", -1) is None:
        output = shellExec("chcp")
        match = re.search(r": (\d{3,})", output or "")

        if match:
            try:
                candidate = "cp%s" % match.group(1)
                codecs.lookup(candidate)
            except LookupError:
                pass
            else:
                kb.codePage = candidate

        kb.codePage = kb.codePage or ""

    if isinstance(value, six.text_type):
        encoding = kb.get("codePage") or getattr(sys.stdout, "encoding", None) or UNICODE_ENCODING

        while True:
            try:
                retVal = value.encode(encoding)
                break
            except UnicodeEncodeError as ex:
                value = value[:ex.start] + "?" * (ex.end - ex.start) + value[ex.end:]

                warnMsg = "cannot properly display (some) Unicode characters "
                warnMsg += "inside your terminal ('%s') environment. All " % encoding
                warnMsg += "unhandled occurrences will result in "
                warnMsg += "replacement with '?' character. Please, find "
                warnMsg += "proper character representation inside "
                warnMsg += "corresponding output files"
                singleTimeWarnMessage(warnMsg)

        if six.PY3:
            retVal = getUnicode(retVal, encoding)

    else:
        retVal = value

    return retVal