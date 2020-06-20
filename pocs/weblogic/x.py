#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   x.py
@Time    :   2020/06/19 17:42:56
@Author  :   - 
@Version :   1.0
@Contact :   huigou90@gmail.com
@License :   Apache License
@Desc    :   None
'''

# here put the import lib

from tic_framework.lib.core.poc import POC
from tic_framework.lib.core.enums import VulLevel , VulType
from tic_framework.lib.core.component import poc_component

@poc_component('X')
class X(POC):
    poc_info = {
        'id' : 1,
        'name': 'POC名称',
        'vulType': VulType.SQLINJECTION,
        'vulLevel': VulLevel.High,
        'vulDate': '漏洞公布时间',
        'createDate': '创建时间',
        'vulNum': ['cve-2020-2551', 'cnvd-2020-111111'],
        'appName': 'app应用名称',
        'appPowerLink': '',
        'appVersion ': ['1.0','2.0'],
        'desc': '''xxxxxxxxxx''',
        'protocol': ''
    }
    
    def _check(self):
        print('_check_')
    
    def _exploit(self):
        print('_exploit_')