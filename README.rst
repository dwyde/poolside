Poolside
========

`Poolside` is a computational notebook system.  It is designed for data
analysis and visualization.

A Tornado-based server communicates with web browsers via HTML5 WebSockets.
Please make sure you are using a browser capable of using WebSockets, such as 
`Chromium <http://www.chromium.org/Home>`_.
    
    To run this software, you will need the following packages:
    
    - `Python <http://python.org>`_ 2.6 or 2.7
    - `CouchDB <http://couchdb.apache.org>`_ 1.0.1 
    - `CouchApp <http://couchapp.org>`_
    - `Tornado <http://github.com/facebook/tornado>`_ 1.1
    - `IPython <http://ipython.scipy.org>`_ 0.11


Instructions and Command Line Arguments
---------------------------------------

* -c: CouchDB database port.  Defaults to 5984.
* -d: Name of the CouchDB database.  Should be "notebook" for now (the default).
* -w: WebSocket server port.  Defaults to 9996 and shouldn't be changed.

Example call:

::

    cd service
    python ws_tornado.py -c 5995
