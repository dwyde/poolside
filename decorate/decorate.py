defaults = {}

class viz_default:
    def __init__(self, *args):
        self.types = args
    
    def __call__(self, func):
        def modified(obj):
            for t in self.types:
                defaults.setdefault(t, func)
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
    
    #reg_test('yikes')
    #reg2('hello there !!!')
    
    data = [5, 4, 3, 'a']
    defaults[data.__class__](data)
    
