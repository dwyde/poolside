#!/usr/bin/env python
#
# Copyright 2011 David Wyde and Chris Hart.
#

import os

import dec

_EXTENSION_DIR = 'viz_ext'

def load_kernel_viz(namespace):
    """Create a global :class:`~dec.Viz` object.
    
    Each notebook kernel has access to its own :class:`~dec.Viz` instance.
    
    :param namespace: A ``locals`` :class:`dict`; a kernel namespace.
    
    For a complete description of the :class:`~dec.Viz` class, please see
    its documentation.
    """
    
    basedir = os.path.split(os.path.abspath(__file__))[0]
    path = os.path.join(basedir, _EXTENSION_DIR)
    viz = dec.Viz([path])
    namespace['Viz'] = viz
