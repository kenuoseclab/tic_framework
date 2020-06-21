#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   cmd.py
@Time    :   2020/06/19 17:47:59
@Author  :   - 
@Version :   1.0
@Contact :   huigou90@gmail.com
@License :   Apache License
@Desc    :   None
'''

# here put the import lib
import sys
import os
import re
import shlex
from argparse import ArgumentParser
from argparse import ArgumentError
from argparse import SUPPRESS
from tic_framework.lib.core.convert import getUnicode
from tic_framework.lib.core.settings import IS_WIN
from tic_framework.lib.core.data import logger

def cmdLineParser(argv=None):
    if not argv:
        argv = sys.argv
    
    # Reference: https://stackoverflow.com/a/4012683 (Note: previously used "...sys.getfilesystemencoding() or UNICODE_ENCODING")
    _ = getUnicode(os.path.basename(argv[0]), encoding=sys.stdin.encoding)
    usage = "%s%s [options]" % ("%s " % os.path.basename(sys.executable) if not IS_WIN else "", "\"%s\"" % _ if " " in _ else _)
    parser = ArgumentParser(usage=usage)
    
    try:
        parser.add_argument("--hh", dest="advancedHelp", action="store_true", help="Show advanced help message and exit")
        parser.add_argument("--version", dest="show_version", action="store_true", help="Show program's version number and exit")
        
         # Target options
        target = parser.add_argument_group('Target', "At least one of these "
                                                     "options has to be provided to define the target(s)")
        target.add_argument("-u", "--url", dest="url", nargs='+',
                            help="Target URL (e.g. \"http://www.site.com/vuln.php?id=1\")")

        target.add_argument("-f", "--file", dest="url_file", help="Scan multiple targets given in a textual file")
        target.add_argument("-r", dest="poc", nargs='+', help="Load POC file from local or remote from seebug website")
        target.add_argument("-m", dest="module", help= "Load Module POC files from local eg:weblogic jboss .")
        target.add_argument("-c", dest="configFile", help="Load options from a configuration INI file")

                # Mode options
        mode = parser.add_argument_group("Mode", "Pocsuite running mode options")

        mode.add_argument("--verify", dest="mode", default='verify', action="store_const", const='verify',
                          help="Run poc with verify mode")
        mode.add_argument("--exploit", dest="mode", action="store_const", const='exploit',
                          help="Run poc with exploit mode")
        
         # Requests options
        request = parser.add_argument_group("Request", "Network request options")
        request.add_argument("--cookie", dest="cookie", help="HTTP Cookie header value")
        request.add_argument("--host", dest="host", help="HTTP Host header value")
        request.add_argument("--referer", dest="referer", help="HTTP Referer header value")
        request.add_argument("--user-agent", dest="agent", help="HTTP User-Agent header value")
        request.add_argument("--random-agent", dest="random_agent", action="store_true", default=False,
                             help="Use randomly selected HTTP User-Agent header value")
        request.add_argument("--proxy", dest="proxy", help="Use a proxy to connect to the target URL")
        request.add_argument("--proxy-cred", dest="proxy_cred", help="Proxy authentication credentials (name:password)")
        request.add_argument("--timeout", dest="timeout", help="Seconds to wait before timeout connection (default 30)")
        request.add_argument("--retry", dest="retry", default=False, help="Time out retrials times.")
        request.add_argument("--delay", dest="delay", help="Delay between two request of one thread")
        request.add_argument("--headers", dest="headers", help="Extra headers (e.g. \"key1: value1\\nkey2: value2\")")

        # Optimization options
        optimization = parser.add_argument_group("Optimization", "Optimization options")
        optimization.add_argument("--plugins", dest="plugins", action="store", default=None,
                                  help="Load plugins to execute")
        optimization.add_argument("--pocs-path", dest="pocs_path", action="store", default=None,
                                  help="User defined poc scripts path")
        optimization.add_argument("--threads", dest="threads", type=int, default=1,
                                  help="Max number of concurrent network requests (default 1)")
        
        args = parser.parse_args()
        if not any((args.url, args.url_file,args.plugins,args.configFile)):
            errMsg = "missing a mandatory option ()"
            errMsg += "Use -h for basic and -hh for advanced help\n"
            parser.error(errMsg)
        return args
    
    except (ArgumentError, TypeError) as ex:
        parser.error(ex)
    
    except SystemExit:
        # Protection against Windows dummy double clicking
        if IS_WIN:
            dataToStdout("\nPress Enter to continue...")
            input()
            raise
    debugMsg = "parsing command line"
    logger.debug(debugMsg)