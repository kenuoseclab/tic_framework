#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   common.py
@Time    :   2020/06/19 17:54:44
@Author  :   - 
@Version :   1.0
@Contact :   huigou90@gmail.com
@License :   Apache License
@Desc    :   None
'''

import sys
import os
import re
import codecs
import collections
import threading
import inspect
from tic_framework.lib.core.data import conf , kb, paths
from tic_framework.lib.core.settings import BANNER, IS_TTY
from tic_framework.thirdparty import six
from tic_framework.lib.core.convert import stdoutEncode
from tic_framework.thirdparty.termcolor.termcolor import colored
from tic_framework.lib.core.decorators import cachedmethod
from tic_framework.lib.core.enums import LOGGING_LEVELS
# here put the import lib



def banner():
    """
    This function prints sqlmap banner with its version
    """

    if not any(_ in sys.argv for _ in ("--version", "--api")) and not conf.get("disableBanner"):
        result = BANNER
        dataToStdout(result, forceOutput=True)


def checkSystemEncoding():
    """
    Checks for problematic encodings
    """

    if sys.getdefaultencoding() == "cp720":
        try:
            codecs.lookup("cp720")
        except LookupError:
            errMsg = "there is a known Python issue (#1616979) related "
            errMsg += "to support for charset 'cp720'. Please visit "
            errMsg += "'http://blog.oneortheother.info/tip/python-fix-cp720-encoding/index.html' "
            errMsg += "and follow the instructions to be able to fix it"
            logger.critical(errMsg)

            warnMsg = "temporary switching to charset 'cp1256'"
            logger.warn(warnMsg)

            _reload_module(sys)
            sys.setdefaultencoding("cp1256")


def weAreFrozen():
    """
    Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located.

    # Reference: http://www.py2exe.org/index.cgi/WhereAmI
    """

    return hasattr(sys, "frozen")


def setPaths(root_path):
    paths.TIC_ROOT_PATH = root_path
    paths.TIC_DATA_PATH = os.path.join(paths.TIC_ROOT_PATH, "data")
    paths.TIC_PLUGINS_PATH = os.path.join(paths.TIC_ROOT_PATH, "plugins")
    paths.TIC_POCS_PATH = os.path.join(paths.TIC_ROOT_PATH, "pocs")



def dataToStdout(data, forceOutput=False, bold=False, contentType=None, coloring=True):
    """
    Writes text to the stdout (console) stream
    """

    if not isinstance(data, six.string_types) and data.startswith("\r"):
        if re.search(r"\(\d+%\)", data):
            data = ""
        else:
            data = "\n%s" % data.strip("\r")

    if not kb.get("threadException"):
        if forceOutput or not (getCurrentThreadData().disableStdOut or kb.get("wizardMode")):
            multiThreadMode = isMultiThreadMode()
            if multiThreadMode:
                logging._acquireLock()

            try:
                if conf.get("api"):
                    sys.stdout.write(stdoutEncode(clearColors(data)), status, contentType)
                else:
                    sys.stdout.write(stdoutEncode(setColor(data, bold=bold) if coloring else clearColors(data)))

                sys.stdout.flush()
            except IOError:
                pass

            if multiThreadMode:
                logging._releaseLock()

            kb.prependFlag = isinstance(data, six.string_types) and (len(data) == 1 and data not in ('\n', '\r') or len(data) > 2 and data[0] == '\r' and data[-1] != '\n')

def setColor(message, color=None, bold=False, level=None, istty=None):
    """
    Sets ANSI color codes

    >>> setColor("Hello World", color="red", istty=True)
    '\\x1b[31mHello World\\x1b[0m'
    >>> setColor("[INFO] Hello World", istty=True)
    '[\\x1b[32mINFO\\x1b[0m] Hello World'
    >>> setColor("[INFO] Hello [CRITICAL] World", istty=True)
    '[INFO] Hello [CRITICAL] World'
    """

    retVal = message

    if message:
        if (IS_TTY or istty) and not conf.get("disableColoring"):  # colorizing handler
            if level is None:
                levels = re.findall(r"\[(?P<result>%s)\]" % '|'.join(_[0] for _ in getPublicTypeMembers(LOGGING_LEVELS)), message)

                if len(levels) == 1:
                    level = levels[0]

            if bold or color:
                retVal = colored(message, color=color, on_color=None, attrs=("bold",) if bold else None)
            elif level:
                try:
                    level = getattr(logging, level, None)
                except:
                    level = None
                retVal = LOGGER_HANDLER.colorize(message, level)
            else:
                match = re.search(r"\(([^)]*)\s*fork\)", message)
                if match:
                    retVal = retVal.replace(match.group(1), colored(match.group(1), color="lightgrey"))

                for match in re.finditer(r"([^\w])'([^\n']+)'", message):  # single-quoted (Note: watch-out for the banner)
                    retVal = retVal.replace(match.group(0), "%s'%s'" % (match.group(1), colored(match.group(2), color="lightgrey")))

        message = message.strip()

    return retVal

def isMultiThreadMode():
    """
    Checks if running in multi-thread(ing) mode
    """

    return threading.activeCount() > 1



@cachedmethod
def getPublicTypeMembers(type_, onlyValues=False):
    """
    Useful for getting members from types (e.g. in enums)

    >>> [_ for _ in getPublicTypeMembers(OS, True)]
    ['Linux', 'Windows']
    """

    retVal = []

    for name, value in inspect.getmembers(type_):
        if not name.startswith("__"):
            if not onlyValues:
                retVal.append((name, value))
            else:
                retVal.append(value)

    return retVal


