def magic_visualize(self, arg):
    '''Visualize data by accessing variables in IPython's user namespace.'''
    
    namespace = getattr(self, 'user_ns')
    if arg in namespace:
        return namespace[arg]
    else:
        raise KeyError('Variable "%s" not found in user namespace.' % (arg,))

def load_ipython_extension(ipython):
    ipython.define_magic('Viz', magic_visualize)
