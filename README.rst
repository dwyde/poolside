Poolside
========

Introduction
------------
`Poolside` is a computational notebook system.  It is designed for data
analysis and visualization.

This software uses CouchDB as both a storage backend and a web server.
A standalone Python HTTP server executes code and returns results, via AJAX.

.. warning ::
  There is currently **NO** security on the Python side. 
  
  Notebooks can access any kernel, and execute any system command as
  the user that runs the `http_server.py` process.

Dependencies
------------
To run this software, you will need the following packages:
    
  - `Python <http://python.org>`_ 2.6 or 2.7
  - `CouchDB <http://couchdb.apache.org>`_ >= 1.0.1
  - `couchdb-python <http://pypi.python.org/pypi/CouchDB>`_ 0.8
  - `CouchApp <http://couchapp.org>`_

Installation into CouchDB
-------------------------
Use CouchApp to initialize and update the files stored in CouchDB ::

  cd notebook
  couchapp push http://localhost:5984/database

Running the Standalone Server
-----------------------------
Example call ::

  cd standalone
  python http_server.py

Command Line Arguments

* ``-c`` : CouchDB database port.  Defaults to 5984.
* ``-s`` : HTTP server port.  Defaults to 8080 and is currently hardcoded
  into the JavaScript (which I need to fix).

Accessing Notebooks
-------------------
Finally, access the following URL in your JavaScript-enabled web browser ::

  http://localhost:5984/database/_design/notebook/_rewrite/nb/test

The last part of the URL (i.e., "test") is the name of notebook. Change it to create new notebooks.