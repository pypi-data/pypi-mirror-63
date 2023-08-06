# -*- coding: utf-8 -*-
from uswarm.loop import Layer, \
    STATE_INIT, STATE_READY, STATE_END,\
    MERGE_ADD


class _TestDoLayer(Layer):
    def _setup__testlayer(self):
        states = {
            STATE_READY: [[], ['hello_world'], []],
        }
        transitions = {
        }
        return states, transitions, MERGE_ADD
    
    def hello_world(self, **kw):
        """adad"""
        print(f"Hello world from DO() in state: {self.state}")
        
class _TestLayer(Layer):
    """A layer that trace activity for check is test has been ok."""

    def _setup__testlayer(self):
        states = {
            STATE_END: [[], ['bye'], []],
        }

        transitions = {
            STATE_READY: {
                'each:5,1': [
                    ['READY', [], ['timer']],
                ],
                'each:5,21': [
                    [STATE_READY, [], ['bye']],
                ],
            },
        }
        return states, transitions, MERGE_ADD

    def start(self, **kw):
        print("Hello World!!")
        self.t0 = time()
        self._func_calls = dict()
        self._log_function()

    def term(self, key, **kw):
        elapsed = time() - self.t0
        print(f"Term {key}: {elapsed}")
        super().term(key, **kw)

    def timer(self, **kw):
        "Empty timer to be overrided"

    def _log_function(self):
        func = get_calling_function(level=2)
        name = func.__func__.__name__
        self._func_calls.setdefault(name, 0)
        self._func_calls[name] += 1

    def _check_log(self, expected):
        """Check if observerd calls match expected ones.
        Expected values can be integer and iterables.
        Ranges may be defined with strings like '7-8'
        """
        for name, _ve in expected.items():
            ve = set()
            for v in flatten(list([_ve])):
                # allow ranges
                v = str(v).split('-')
                v.append(v[0])
                ve.update(range(int(v[0]), int(v[1]) + 1))

            vr = self._func_calls.get(name, None)
            if vr not in ve:
                self.reactor.stop()
                raise RuntimeError(f"Fuction {name} is expected to be called {ve} time, but where {vr}")
