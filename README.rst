Poolside
========

Introduction
------------
`Poolside` is a computational notebook system.  It is designed for data
analysis and visualization.

This software uses CouchDB as both a storage backend and a web server.
A standalone Python HTTP server executes code and returns results, via AJAX.

Warning
-------
  There is currently **NO** security on the Python HTTP server.
  
  Notebooks can access any kernel, and execute any system command as
  the user that runs the `http_server.py` process.

Dependencies
------------
To run this software, you will need the following packages:
    
  - `Python <http://python.org>`_ 2.6 or 2.7
  - `CouchDB <http://couchdb.apache.org>`_ >= 1.0.1
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

Other configuration options

* This server defaults to running on ``localhost:8282``.

  Set in poolside/notebook/_attachments/server.txt, so that it can be shared
  by CouchDB and the standalone server.

Accessing Notebooks
-------------------
Finally, access the following URL in your JavaScript-enabled web browser ::

  http://localhost:5984/database/_design/notebook/_rewrite/poolside/test

The last part of the URL (i.e., "test") is the name of notebook. Change it to create new notebooks.