#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   option.py
@Time    :   2020/06/19 20:51:22
@Author  :   - 
@Version :   1.0
@Contact :   huigou90@gmail.com
@License :   Apache License
@Desc    :   None
'''

# here put the import lib
import os
import importlib
from queue import Queue
from tic_framework.lib.core.datatype import AttribDict , OrderedSet
from tic_framework.lib.core.data import conf, kb, paths,  mergedOptions, cmdLineOptions


def _setConfAttributes():
    conf.url = None
    conf.url_file = None
    conf.mode = 'check'
    conf.poc = None
    
    # module pocs
    conf.module = None
    conf.cookie = None
    conf.host = None
    conf.referer = None
    conf.agent = None
    conf.headers = None
    conf.random_agent = None
    conf.proxy = None
    conf.proxy_cred = None
    conf.proxies = {}
    conf.timeout = 30
    conf.retry = 0
    conf.delay = 0
    conf.http_headers = {}
    # threads
    conf.threads = 1


def _setKbAttributes():
    kb.registered_pocs = AttribDict()
    kb.task_queue = Queue()
    kb.targets = OrderedSet()


def _mergeOptions(inputOptions, overrideOptions):
    if hasattr(inputOptions, "items"):
        inputOptionsItems = inputOptions.items()
    else:
        inputOptionsItems = inputOptions.__dict__.items()
    
    for key, value in inputOptionsItems:
        if key not in conf or value not in (None, False) or overrideOptions:
            conf[key] = value

    mergedOptions.update(conf)


def initOptions(inputOptions=AttribDict(), overrideOptions=False):
    cmdLineOptions.update(inputOptions)
    _setConfAttributes()
    _setKbAttributes()
    _mergeOptions(inputOptions, overrideOptions)
    
    init()


def init():
    _set_multiple_targets()
    _set_pocs()
    _set_task_queue()


def _set_multiple_targets():
    if conf.url:
        targets  = set()
        for url in conf.url:
            targets.add(url)
        
        for target in targets:
            kb.targets.add(target)
    
    if conf.url_file:
        for line in get_file_items(conf.url_file, lowercase=False, unique=True):
            kb.targets.add(line)


def _set_pocs():
    #print(conf.poc)
    if conf.poc:
        for poc in conf.poc:
            module = importlib.import_module(poc.replace('/','.').replace('.py',''))
            #print(module)


def _set_task_queue():
    if not kb.registered_pocs:
        err_msg = "no pocs  script load"
        logger.error(err_msg)
    
    if not kb.targets:
        err_msg = "no target(s) was added!"
        logger.error(err_msg)
    
    # print(kb.registered_pocs)
    # print(kb.targets)
    
    if kb.registered_pocs and kb.targets:
        for poc_module in kb.registered_pocs:
            for target in kb.targets:
                kb.task_queue.put((poc_module, target))