#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   data.py
@Time    :   2020/06/19 21:35:30
@Author  :   - 
@Version :   1.0
@Contact :   huigou90@gmail.com
@License :   Apache License
@Desc    :   None
'''

# here put the import lib

from tic_framework.lib.core.datatype import AttribDict
from tic_framework.lib.core.log import LOGGER

# tic_framework paths
paths = AttribDict()

# object to store original command line options
cmdLineOptions = AttribDict()

# object to store merged options (command line, configuration file and default options)
mergedOptions = AttribDict()

# line options and settings
conf = AttribDict()

# object to share within function and classes results
kb = AttribDict()

# logger
logger = LOGGER