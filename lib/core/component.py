#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   component.py
@Time    :   2020/06/20 11:07:18
@Author  :   - 
@Version :   1.0
@Contact :   huigou90@gmail.com
@License :   Apache License
@Desc    :   None
'''

# here put the import lib

from tic_framework.lib.core.data import kb

def poc_component(plugin_name):
    def wrapper(plugin):
        kb.registered_pocs[plugin_name] = plugin()
        return
    return wrapper