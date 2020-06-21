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
from tic_framework.lib.core.enums import VulLevel, VulType, POC_FAMILY
from tic_framework.lib.core.component import poc_component


@poc_component('cve_2020_2551')
class cve_2020_2551(POC)
    poc_info = {
        'id' : 2,
        'name': 'Oracle WebLogic CVE-2020-2551 IIOP反序列化命令执行漏洞',
        'vulType': VulType.Serialization,
        'vulLevel': VulLevel.High,
        'vulDate': '2020-05-21',
        'createDate': '2020-05-21',
        'References': [''],
        'vulNum': ['cve-2020-2551', 'cnvd-2020-111111'],
        'appName': 'app应用名称',
        'appPowerLink': 'http://www.oracle.com',
        'appVersion ': ['10.3.6','12.3.0'],
        'desc': '''Oracle WebLogic CVE-2020-2551 IIOP反序列化远程命令执行漏洞''',
        'protocol': POC_FAMILY.PROTOCOL.T3
    }
    
    def _verify(self):
        print('_verify_')
        print(self.rhost)
        print(self.rport)
        print(self.ssl)
    
    def _exploit(self):
        print('_exploit_')