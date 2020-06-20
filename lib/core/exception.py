#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   exception.py
@Time    :   2020/06/19 22:14:18
@Author  :   - 
@Version :   1.0
@Contact :   huigou90@gmail.com
@License :   Apache License
@Desc    :   None
'''

# here put the import lib


class TicBaseException(Exception):
    pass

class TicConnectionException(TicBaseException):
    pass

class TicThreadException(TicBaseException):
    pass

class TicUserQuitException(TicBaseException):
    pass

class TicValueException(TicBaseException):
    pass