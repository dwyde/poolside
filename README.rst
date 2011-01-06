Command line arguments to service/ws_tornado.py:

* -c: CouchDB database port.  Defaults to 5984.
* -d: Name of the CouchDB database.  Should be "notebook" for now (the default).
* -w: WebSocket server port.  Defaults to 9996 and shouldn't be changed.

Example call:

::

    cd service
    python ws_tornado.py -c 5995
