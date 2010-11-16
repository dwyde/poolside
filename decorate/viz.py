class VizDecor:
    """ A class that creates decorator functions for visualizable objects """
    def __init__(self, acceptDict):
        """acceptDict is of the form {obj:acceptorFuction, ...}  
        
        such that acceptorFunction[type(obj)](obj) --> True when the obj is appropriate for the fuction being decorarted.
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

        return newFunc


#### EXAMPLE ###
@VizDecor({str: lambda x: len(x) < 10,
           list: lambda x: len(x) < 10 })
def test(foo):
    print foo


##################

def main():
    #test(range(5))
    test(range(11))

if __name__ == '__main__':
    main()
