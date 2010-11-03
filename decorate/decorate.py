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

class Viz:
    defaults = {}
        
    @classmethod
    def add_method(cls, obj_type, method):
        cls.defaults.setdefault(obj_type, method)

class viz_default:
    def __init__(self, *args):
        self.types = args
    
    def __call__(self, func):
        def modified(obj):
            for t in self.types:
                Viz.add_method(t, func)
            func(obj)
        return modified
    
@viz_default(list, tuple)
def reg_test(obj):
    print 'yes!'
    
@viz_default(int, basestring)
def reg2(obj):
    print obj

@viz_default(list, basestring)
def reg1(obj):
    print obj
        
if __name__ == '__main__':
    #print2('hello')
    #print2(['hello'])
    #print '*' * 5
    #print_all('hello')
    #print_all(['hello'])
    ##reg1('hello')
    ##reg2('okay')
    reg_test('yikes')
    reg2('hello there !!!')
    
    #data = [5, 4, 3, 'a']
    #registry[data.__class__](t, data)
    
