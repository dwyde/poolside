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
        def modified(viz_obj, data):
            for t in self.types:
                registry.setdefault(t, func)
            print registry
            func(viz_obj, data)
        return modified
    
class Test:
    @viz_default(list, tuple)
    def reg_test(self, obj):
        print 'yes!'
        
    @viz_default(int, basestring)
    def reg2(self, obj):
        print obj

    @viz_default(list, basestring)
    def reg1(self, obj):
        print obj
        
if __name__ == '__main__':
    #print2('hello')
    #print2(['hello'])
    #print '*' * 5
    #print_all('hello')
    #print_all(['hello'])
    ##reg1('hello')
    ##reg2('okay')
    t = Test()
    t.reg_test('yikes')
    t.reg2('hello there !!!')
    
    data = [5, 4, 3, 'a']
    registry[data.__class__](t, data)
    
