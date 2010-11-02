class allows:
    def __init__(self, *args):
        self.permitted = args
    
    def __call__(self, func):
        def modified(obj):
            maybe = map(lambda x: isinstance(obj, x), self.permitted)
            if filter(None, maybe): # If the above list has any "True" elements
                func(obj)
            else:
                print "%s not allowed for this function.  You must use one of %s." % \
                        (type(obj), self.permitted)
        return modified

@allows(int, list)
def print2(word):
    print word
    
if __name__ == '__main__':
    print2('hello')
    print2(['hello'])
