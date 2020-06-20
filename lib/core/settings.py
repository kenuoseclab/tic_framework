#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   settings.py
@Time    :   2020/06/19 21:15:24
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
import random


# colorful banner
BANNER = """\033[01;33m\
        ___
       __H__
 ___ ___[.]_____ ___ ___  \033[01;37m{\033[01;\033[01;37m}\033[01;33m
|_ -| . [.]     | .'| . |
|___|_  [.]_|_|_|__,|  _|
      |_|V...       |_|   \033[0m\033[4;37m\033[0m\n
"""

HEURISTIC_CHECK_ALPHABET = ('"', '\'', ')', '(', ',', '.')

# Minor artistic touch
BANNER = re.sub(r"\[.\]", lambda _: "[\033[01;41m%s\033[01;49m]" % random.sample(HEURISTIC_CHECK_ALPHABET, 1)[0], BANNER)

IS_TTY = hasattr(sys.stdout, "fileno") and os.isatty(sys.stdout.fileno())

PLATFORM = os.name
IS_WIN = PLATFORM == "nt"


UNICODE_ENCODING = "utf8"
MAX_CACHE_ITEMS = 256

MAX_NUMBER_OF_THREADS = 50