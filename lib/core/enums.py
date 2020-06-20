#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   enums.py
@Time    :   2020/06/19 21:34:54
@Author  :   - 
@Version :   1.0
@Contact :   huigou90@gmail.com
@License :   Apache License
@Desc    :   None
'''

# here put the import lib
from tic_framework.lib.core.datatype import AttribDict

class LOGGING_LEVELS(object):
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class CUSTOM_LOGGING(object):
    PAYLOAD = 9
    TRAFFIC_OUT = 8
    TRAFFIC_IN = 7


class PAYLOAD(object):
    pass

class VulType:
    SQLINJECTION = 'SQL注入漏洞'
    XSS = 'XSS跨站脚本漏洞'
    CSRF = '客户端请求伪造漏洞'
    SSRF = '服务器端请求伪造漏洞'
    XXE = 'XML实体注入漏洞'
    RCE = '远程命令执行漏洞'
    WEAKPASSORD = '弱口令漏洞'
    Serialization = '反序列化漏洞'
    UNAUTHORIZED_ACCESS = '未授权访问漏洞'
    UPLOAD_FILES = '任意文件上传漏洞'
    FILES_OPERATION = '文件操作漏洞'
    DirectoryTraversal = '目录穿越漏洞'
    InfoLeak = '信息泄漏漏洞'
    MISConfiguration = '配置错误漏洞'
    SSTI = '模版注入漏洞'
    XQUERY_INJECTION = 'XQuery注入漏洞'
    DENIAL_OF_SERVICE = '拒绝服务漏洞'

class VulLevel:
    High = '高'
    Medium = '中'
    Low = '低'

class POC_FAMILY:
    '''
        Protocol Type
    '''
    PROTOCOL = AttribDict()
    PROTOCOL.TCP = 'tcp'
    PROTOCOL.HTTP = 'http'
