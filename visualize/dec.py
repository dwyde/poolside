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
        
        In this example, calling :meth:`Viz` on a :class:`list` will not
        always produce the desired result.
        
        This will be fixed in a future version, but it is broken right now.
    """
    
    def __init__(self, ext_dirs):
        self.typemap = collections.defaultdict(list)
        ext_files = []
        # Make this class available in extension functions.
        globals_dict = {'Viz': self}
        locals_dict = {}
        for ext_dir in ext_dirs:
            ext_files.extend(glob.glob(os.path.join(ext_dir, '*.py')))
        for ext_file in ext_files:
            execfile(ext_file, globals_dict, locals_dict)
        for name, func in locals_dict.items():
            if type(func) == types.FunctionType:
                for t, acceptor in func(None).items():
                    self.typemap[t].append((acceptor, func))
                setattr(self, name, func)
    
    def __call__(self, obj):
        """Call an appropriate extension function for `obj`.
        
        Dispatch a :class:`~dec.VizDecor` function based on the
        :class:`type` of `obj`.
        
        In a notebook frontend::
            
            print Viz([1, 2, 'a'])
        """
        
        if type(obj) in self.typemap:
            for acceptor, func in self.typemap[type(obj)]:
                if acceptor(obj):
                    return func(obj)

        # Do the default thing.
        return str(obj)

class VizDecor:
    """ A class that creates decorator functions for visualizable objects.
    
    :param accept_dict: a :class:`dict` of the form ``{type: acceptorFunction}``::
        
            @VizDecor({list: lambda x: len(x) < 5})
            def table(obj):
                return '* %s *' % str(obj)
        
        ``acceptorFunction(obj)`` should return ``True`` when `obj` is 
        appropriate for the fuction being decorated.
    """
    
    def __init__(self, accept_dict):
        self.accept_dict = accept_dict
        
    def __call__(self, func):
        """Decorate a visualization function :func:`func`.
        
        :func:`func` should take a single argument: `obj`, a Python object
        to visualize.  This object must meet the constraints defined in
        ``self.accept_dict``.
        
        .. note:: :meth:`~dec.Viz` can be called recursively by extension functions.
            
            This allows for the visualization of nested data structures.
        """
        
        def newFunc(obj):
            """Decorate a visualization extension function.
            
            :param obj: An object to visualize.
            :return: A list of acceptable types, if `obj` is None. Otherwise,
            the original function.
            
            Notebook frontends should never raise a :class:`TypeError` 
            below, because the Viz.__call__() method will just return str()
            on any "illegal" objects.
            """
            
            if obj is None:
                return self.accept_dict
            else:
                if type(obj) in self.accept_dict:
                    if self.accept_dict[type(obj)](obj):
                       return func(obj)
                    else:
                        raise TypeError('type supported, instance not supported')
                else:
                    raise TypeError('object type not supported')

        return newFunc
