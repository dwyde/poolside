ALL = '*'

class allows:
    def __init__(self, *args):
        self.permitted = args
    
    def __call__(self, func):
        def modified(obj):
            if self.permitted == (ALL,):
                func(obj)
            else:
                maybe = map(lambda x: isinstance(obj, x), self.permitted)
                if any(maybe): # If the above list has any "True" elements
                    func(obj)
                else:
                    print "%s not allowed for this function.  You must use one of %s." % \
                            (type(obj), self.permitted)
        return modified

@allows(int, basestring)
def print2(word):
    print word
    
@allows(ALL)
def print_all(word):
    print word

# # # # # # # #

registry = {}

class viz_default:
    def __init__(self, *args):
        self.types = args
    
    def __call__(self, func):
        def modified(obj):
            for t in self.types:
                registry.setdefault(t, func)
            print registry
            func(obj)
        return modified

@viz_default(list, basestring)
def reg1(word):
    print word
        
if __name__ == '__main__':
    #print2('hello')
    #print2(['hello'])
    #print '*' * 5
    #print_all('hello')
    #print_all(['hello'])
    reg1('hello')
    data = [5, 4, 3, 'a']
    registry[data.__class__](data)