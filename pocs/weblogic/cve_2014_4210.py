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
from tic_framework.lib.core.enums import POC_FAMILY

@poc_component('cve_2014_4210')
class cve_2014_4210(POC):
    poc_info = {
        'id' : 1,
        'name': 'Oracle WebLogic /uddiexplorer/ 应用SSRF服务器端请求伪造漏洞',
        'vulType': VulType.SSRF,
        'vulLevel': VulLevel.Low,
        'vulDate': '2014-04-21',
        'createDate': '2020-01-02',
        'References': [''],
        'vulNum': ['cve-2014-4210', 'cnvd-2020-111111'],
        'appName': 'weblogic',
        'appPowerLink': 'http://www.oracle.com',
        'appVersion ': ['10.3.6'],
        'desc': '''Weblogic /uddiexplorer/ 存在SSRF服务器端请求伪造漏洞, 利用该可以进行目标主机网络探索等攻击行为''',
        'protocol': POC_FAMILY.PROTOCOL.HTTP
    }
    

    def _verify(self):
        print('_verify_')
        print(self.url)

        result = {}
    

    

    def _exploit(self):
        print('_exploit_')