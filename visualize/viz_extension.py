import os

import dec

def magic_visualize(self, arg):
    '''Visualize data by accessing variables in IPython's user namespace.'''
    
    namespace = getattr(self, 'user_ns')
    if arg in namespace:
        return self._visualize(namespace[arg])
    else:
        raise KeyError('Variable "%s" not found in user namespace.' % (arg,))

def load_ipython_extension(user_ns):
    '''A setup function, called each time this extension is loaded.'''
    basedir = os.path.split(os.path.abspath(__file__))[0]
    path = os.path.join(basedir, 'viz_ext')
    viz = dec.Viz([path])
    user_ns['Viz'] = viz
