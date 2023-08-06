#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module test Loop features
"""
import time
import functools

import pytest

from uswarm.loop import Layer, Loop
    #STATE_INIT, STATE_READY, STATE_END,\
    # MERGE_ADD
    

# --------------------------------------------------
# logger
# --------------------------------------------------
from gutools.loggers import logger, trace, debug, info, warn, error, exception
log = logger(__name__)

from .helpers import _TestDoLayer

class FakeEventInjector():
    """Helper class to inject some events from time to time
    using a local socket as transport layer.
    """
    
class FakeServer():
    """"""

class FakeClient():
    """"""

#from .helpers import _TestLayer

#class Clock(_TestLayer):

    #def _setup_test_clock(self):
        #states = {
        #}
        # transitions = {
            #STATE_READY: {
                # set an additional timer
                # 'each:3,2': [
                    #[STATE_READY, [], ['timer']],
                #],
            #},
        #}
        # return states, transitions, MERGE_ADD

@pytest.fixture
def loop():
    loop = Loop()
    return loop

def test_minimal_layer(loop):
    """"
    - [ ] Create minimal Layer and Loop
    - [ ] Start and End loop
    """
    layer = Layer()
    loop.attach(layer)

    loop.run()
    foo = 1

def test_layer_definition(loop):
    """"
    - [ ] Load a STM definition from a file
    - [ ] Bind (strict=False) with a class / instance which such methods
    - [ ] Bind (strict=True) with a class / instance which a missing method
    - [ ] Bind with an external class / instance which doesn't inherit from Layer
    """
    layer = Layer()
    loop.attach(layer)
    
def test_entry_exit_state_functions(loop):
    """"
    - [ ] xxxx
    """
    layer = Layer()
    loop.attach(layer)
    loop.run()
    
def test_do_state_functions(loop):
    """"
    - [ ] xxxx
    """
    layer = _TestDoLayer()
    loop.attach(layer)
    loop.run()
    foo =1

def test_timers(loop):
    """"
    - [ ] Test Timeout
    - [ ] Test Restarting Timer
    - [ ] Test Restarting Timer with Timeout
    """
    foo = 1
    trace()
    
    
def test_stm_sharing_same_context(loop):
    """"
    - [ ] Stack many layers that respond to the same event buy they share the same context (STM)
    """


def test_connect():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """
    time.sleep(0)

def test_listen():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_attaching_existing_protocol():
    """
    - [ ] connect to somewhere and attach a STM
    - [ ] search for an existing connection
    - [ ] attach to existing connection
    """
    time.sleep(0)


def test_multiples_reactors():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """
    time.sleep(0)

def test_serialize_app():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """
    time.sleep(0)

def test_register_protocols():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """
    time.sleep(0)

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """
    time.sleep(0)

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """
    time.sleep(0)

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """
    time.sleep(0)

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """
    time.sleep(0)

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """
    time.sleep(0)

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """
    time.sleep(0)

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """
    time.sleep(0)

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

