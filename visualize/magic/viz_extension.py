import dec

def magic_visualize(self, arg):
    '''Visualize data by accessing variables in IPython's user namespace.'''
    
    namespace = getattr(self, 'user_ns')
    if arg in namespace:
        return self._visualize(namespace[arg])
    else:
        raise KeyError('Variable "%s" not found in user namespace.' % (arg,))

def load_ipython_extension(ipython):
    '''A setup function, called each time this extension is loaded.'''
    viz = dec.Viz(['viz_ext'])
    ipython._visualize = viz
    ipython.define_magic('Viz', magic_visualize)
