import types
import os
import glob
import collections


class Viz:
    def __init__(self, extdirs):
        """ Construct a dynamic viz dispatching function """
        self.typemap = collections.defaultdict(list)
        extFiles = []
        globalsDict = {}
        localsDict = {}
        for d in extdirs:
          extFiles.extend(glob.glob(os.path.join(d, '*.py')))
        for f in extFiles:
          execfile(f, globalsDict, localsDict)
        for name, func in localsDict.items():
            if type(func) == types.FunctionType:
                for t,acceptor in func(None).items():
                    self.typemap[t].append((acceptor, func))
                setattr(self, name, func)
    def __call__(self, obj):
        if type(obj) in self.typemap:
            for acceptor, func in self.typemap[type(obj)]:
                if acceptor(obj):
                    return(func(obj))
        ## Do The default thing
        return(str(obj))




class VizDecor:
    """ A class that creates decorator functions for visualizable objects """
    def __init__(self, acceptDict):
        """acceptList is a list of tuples of the form [(obj, acceptorFuction)...]  
        
        acceptorFunction(obj) --> True when the obj is appropriate for the fuction being decorarted.
        """
        self.acceptDict = acceptDict
    def __call__(self, f):
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

        return(newFunc)
