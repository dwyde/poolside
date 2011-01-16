#!/usr/bin/env python
#
# Copyright 2011 Chris Hart and David Wyde.
#

import types
import os
import glob
import collections

class Viz:
    """Dynamically visualize Python objects based on their :class:`type`.
    
    `extdirs` is a :class:`list` of directories to search for ".py" files.
    Each function in these Python scripts should be decorated by 
    :class:`~dec.VizDecor`.
    
    .. warning:: There is currently no way to choose between different \
    :class:`Viz` extension functions that apply to the same :class:`type`.
    
        Please DO NOT decorate two functions with the same type::
            
            @VizDecor({list: lambda x: len(x) < 5})
            def small_table(obj):
                ...
            
            @VizDecor({list: lambda x: len(x) >= 5})
            def big_table(obj):
                ...
        
        In this example, calling :class:`Viz` on a :class:`list` will not
        always produce the desired result.
        
        This will be fixed in a future version, but it is broken right now.
    """
    
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
