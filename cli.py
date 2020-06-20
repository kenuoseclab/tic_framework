#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   cli.py
@Time    :   2020/06/19 18:40:11
@Author  :   - 
@Version :   1.0
@Contact :   huigou90@gmail.com
@License :   Apache License
@Desc    :   None
'''

# here put the import lib
import sys
import os
import inspect
import traceback
import threading
import distutils
from tic_framework.lib.core.common import weAreFrozen
from tic_framework.lib.core.convert import getUnicode
from tic_framework.lib.core.common import setPaths
from tic_framework.lib.parse.cmdline import cmdLineParser
from tic_framework.lib.core.data import logger , kb
from tic_framework.lib.core.common import banner
from tic_framework.lib.core.option import initOptions
from tic_framework.lib.controller.controller import start

def modulePath():
    """
    This will get us the program's directory, even if we are frozen
    using py2exe
    """
    
    try:
        _ = sys.executable if weAreFrozen() else __file__
    except NameError:
        _ = inspect.getsourcefile(modulePath)
    
    return getUnicode(os.path.dirname(os.path.realpath(_)), encoding=sys.getfilesystemencoding() or UNICODE_ENCODING)


def checkEnvironment():
    # print(modulePath())
    try:
        os.path.isdir(modulePath())
    except UnicodeEncodeError:
        errMsg = "your system does not properly handle non-ASCII paths. "
        errMsg += "Please move the sqlmap's directory to the other location"
        logger.critical(errMsg)
        raise SystemExit


def main():
    checkEnvironment()
    setPaths(modulePath())
    banner()
    initOptions(cmdLineParser().__dict__)
    
    start()
    # print(kb.registered_pocs)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except SystemExit:
        pass
    except:
        traceback.print_exc()
    finally:
        if threading.activeCount() > 1:
            os._exit(getattr(os, "_exitcode", 0))
        else:
            sys.exit(getattr(os, "_exitcode", 0))