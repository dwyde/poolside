#!/usr/bin/env python
#
# Copyright 2011 Chris Hart and David Wyde.
#

import types
import os
import glob
import collections

class Viz:
    """ Construct a dynamic viz dispatching function """
    
    def __init__(self, extdirs):
        self.typemap = collections.defaultdict(list)
        extFiles = []
        # Make this class available in extension functions.
        globalsDict = {'Viz': self}
        localsDict = {}
        for d in extdirs:
            extFiles.extend(glob.glob(os.path.join(d, '*.py')))
        for f in extFiles:
            execfile(f, globalsDict, localsDict)
        for name, func in localsDict.items():
            if type(func) == types.FunctionType:
                for t, acceptor in func(None).items():
                    self.typemap[t].append((acceptor, func))
                setattr(self, name, func)
    
    def __call__(self, obj):
        if type(obj) in self.typemap:
            for acceptor, func in self.typemap[type(obj)]:
                if acceptor(obj):
                    return func(obj)

        # Do the default thing.
        return str(obj)

class VizDecor:
    """ A class that creates decorator functions for visualizable objects.
    
    :param acceptDict: a :class:`dict` of the form ``{type: acceptorFunction}``::
        
            @VizDecor({list: lambda x: len(x) < 5})
            def table(obj):
                return '* %s *' % str(obj)
        
        ``acceptorFunction(obj)`` should return ``True`` when `obj` is 
        appropriate for the fuction being decorated.
    """
    
    def __init__(self, acceptDict):
        self.acceptDict = acceptDict
        
    def __call__(self, f):
        """Decorate a visualization function :func:`f`.
        
        :func:`f` should take a single argument: `obj`, a Python object
        to visualize.  This object must meet the constraints defined in
        ``self.acceptDict``.
        """
        
        # Notebook frontends should never raise a :class:`TypeError` below,
        # because the Viz.__call__() method will just return str() on any
        # "illegal" objects.
        
        def newFunc(obj):
            if obj == None:
                return self.acceptDict
            else:
                if type(obj) in self.acceptDict:
                    if self.acceptDict[type(obj)](obj):
                       return f(obj)
                    else:
                        raise TypeError('type supported, instance not supported')
                else:
                    raise TypeError('object type not supported')

        return newFunc
