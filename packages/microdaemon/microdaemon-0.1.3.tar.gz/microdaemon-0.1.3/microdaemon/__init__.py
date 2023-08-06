
# https://github.com/eventlet/eventlet/issues/592
# import eventlet
# eventlet.monkey_patch()

import eventlet
import eventlet.green.threading
try: 
    eventlet.green.threading.__patched__.remove('_after_fork')
except ValueError: 
    pass
eventlet.monkey_patch()
import __original_module_threading
import threading
__original_module_threading.current_thread.__globals__['_active'] = threading._active
threading._after_fork.__globals__['current_thread'] = __original_module_threading.current_thread

import sys

from . import jsonlib
jsonlib.json_settings()

from . import configclass

name="microdaemon"

__all__ = ["abstracts", "channels", "common", "config","configclass",
           "configurator","database","jsonlib","pages",
           "responses","server","threads"]

class ConfigWrapper(object):
    
    def __init__(self,actual):
        self._actual=actual

    def setup(self,actual):
        self._actual=actual

    def __repr__(self): return self._actual.__repr__()
    def __str__(self): return self._actual.__str__()
    def __dir__(self): return self._actual.__dir__()

    def __getattr__(self,name): 
        if name in ["_actual","setup"]: return object.__getattr__(self,name)
        return self._actual.__getattr__(name)

    def __getattribute__(self,name): 
        if name in ["_actual","setup"]: return object.__getattribute__(self,name)
        return self._actual.__getattribute__(name)

    def __delattr__(self,name): 
        if name in ["_actual","setup"]: return
        return self._actual.__delattr__(name)

    def __setattr__(self,name,value): 
        if name in ["_actual","setup"]: 
            object.__setattr__(self,"_actual",value)
            return
        return self._actual.__setattr__(name,value)
    
sys.modules[__name__+".config"]=ConfigWrapper

config=ConfigWrapper(configclass.Config())
