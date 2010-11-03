class Viz:
    defaults = {}
    
    def __call__(self, obj):
        return self.defaults[obj.__class__](obj)
        
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
    return obj
    
@viz_default(int, basestring)
def reg2(obj):
    print obj

@viz_default(list, basestring)
def reg1(obj):
    print 1
    return obj
        
if __name__ == '__main__':
    v = Viz()
    
    reg_test('yikes')
    #reg2('hello there !!!')
    
    print v( (5, 4, 3) )
    
    #data = [5, 4, 3, 'a']
    #registry[data.__class__](t, data)
    
