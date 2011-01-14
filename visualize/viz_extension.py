#!/usr/bin/env python
#
# Copyright 2011 David Wyde and Chris Hart.
#

import os

import dec

def load_ipython_extension(user_ns):
    '''A setup function, called each time this extension is loaded.'''
    basedir = os.path.split(os.path.abspath(__file__))[0]
    path = os.path.join(basedir, 'viz_ext')
    viz = dec.Viz([path])
    user_ns['Viz'] = viz
