# coding=UTF-8
# ex:ts=4:sw=4:et=on

# Copyright (c) 2013, Mathijs Dumon
# All rights reserved.
# Complete license can be found in the LICENSE file.

from contextlib import contextmanager, ExitStack

class EventContextManager(object):
    """
        Event context manager class, to be used as follows:
        
         ecm = EventContextManager(model.event1, model.event2, ...)
        
         with ecm.ignore():
             pass #do something here that will cause events to be ignored
        
         with ecm.hold():
             pass #do something here that will cause events to be held back
        
    """
    
    events = []
    
    def __init__(self, *events):
        self.events = events
        
    @contextmanager
    def ignore(self):
        if len(self.events):
            with ExitStack() as stack:
                for event in self.events:
                    stack.enter_context(event.ignore())
                yield
        else:
            yield

    @contextmanager
    def hold(self):
        if len(self.events):
            with ExitStack() as stack:
                for event in self.events:
                    stack.enter_context(event.hold())
                yield
        else:
            yield

    pass #end of class