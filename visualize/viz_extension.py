#!/usr/bin/env python
#
# Copyright 2011 David Wyde and Chris Hart.
#

import os

import dec

_EXTENSION_DIR = 'viz_ext'

def load_ipython_extension(namespace):
    """A setup function, called each time this extension is loaded."""
    
    basedir = os.path.split(os.path.abspath(__file__))[0]
    path = os.path.join(basedir, _EXTENSION_DIR)
    viz = dec.Viz([path])
    namespace['Viz'] = viz
