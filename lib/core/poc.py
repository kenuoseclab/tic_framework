#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   poc.py
@Time    :   2020/06/21 08:38:47
@Author  :   - 
@Version :   1.0
@Contact :   huigou90@gmail.com
@License :   Apache License
@Desc    :   None
'''

# here put the import lib
from urllib.parse import urlparse
from tic_framework.lib.core.datatype import OrderedDict
from tic_framework.lib.core.enums import POC_FAMILY

class POC(object):
    def __init__(self):
        self.target = None
        self.url = None
        self.path = None
        self.params = None
        self.mode = None
        self.headers = None
        self.protocol = getattr(self, "poc_info")['protocol']
        self.pocDesc = getattr(self,"poc_info")['desc']

        #register_options
        self.options = OrderedDict()
        if self.protocol == POC_FAMILY.PROTOCOL.HTTP:
            self.options['target'] = 'http://127.0.0.1'
            self.options['timeout'] = 30
            self.options['referer'] = ''
        else:
            self.options['rhost'] = '127.0.0.1'
            self.options['rport'] = int(0)
            self.options['ssl'] = False

    def build_target(self):
        if self.target:
            if self.protocol == POC_FAMILY.PROTOCOL.HTTP:
                self.url = self.target
            else:
                upe = urlparse(self.target)
                self.rport = upe.port if upe.port else 0
                self.rhost = upe.hostname
                if upe.scheme == 'https':
                    self.ssl = True
        return

    def auto_execute(self, target, mode= 'check'):
        self.target = target
        self.mode = mode
        # Analyze build targets
        self.build_target()
        if self.mode == 'verify':
            self._verify()
        elif self.mode == 'exploit':
            self._exploit()


    def _verify(self):
        raise NotImplementedError
    
    
    def _exploit(self):
        raise NotImplementedError


class Output(object):
    def __init__(self):
        self.status = False
        self.data = {
            'exploit': {
                
            },
            'verify': {

            }
        }
        self.description = ''
        self.error = ''
    
    def success(self):
        pass

    
    def fail(self):
        pass
