Poolside
========

Introduction
------------
`Poolside` is a computational notebook system.  It is designed for data
analysis and visualization.

This software uses CouchDB as both a storage backend and a web server.
A standalone Python HTTP server executes code and returns results, via AJAX.

Security Warning
----------------
The only current security feature on the Python server is resource limits.
  
Notebooks can access any kernel, and execute any system command as
the user that runs the `http_server.py` process.

Chroot jails are coming soon.

Dependencies
------------
To run this software, you will need the following packages:
    
  - `Python <http://python.org>`_ 2.6 or 2.7
  - `CouchDB <http://couchdb.apache.org>`_ >= 1.0.1
  - `CouchApp <http://couchapp.org>`_
  - `Ruby <http://www.ruby-lang.org/en/>`_ >= 1.9.1 (to make Ruby kernels work)

Installation into CouchDB
-------------------------
Use CouchApp to initialize and update the files stored in CouchDB ::

  cd poolside/notebook
  couchapp push http://localhost:5984/database

Server Configuration
--------------------
Both the JavaScript notebook frontend (in CouchDB) and the evaluation server
(Python) need to know the eval server's port. The current approach is to store
a JSON file ::

  poolside/notebook/eval_server.json

that defines the port to which the notebook will send its evaluation requests.
When the eval server starts up, it will ask CouchDB for this address.

Running the Standalone Server
-----------------------------
Example call ::

  cd poolside/standalone
  python http_server.py -c http://localhost:5984/database/_design/notebook/eval_server.json

Command Line Arguments

-c config_file        Full URL of a server configuration file attached to the 
                      CouchApp's design document. Required.

Accessing Notebooks
-------------------
Finally, access the following URL in your JavaScript-enabled web browser ::

  http://localhost:5984/database/_design/notebook/_rewrite/poolside/test

The last part of the URL (i.e., "test") is the name of notebook. Change it to create new notebooks.

Random Points
-------------
This project has had a number of different architectures, so its documentation
may lag behind the actual code.

Make sure you are logged in before trying to edit any cell data. The easy
way for now is to look at the bottom right corner of ::

  localhost:5984/_utils.

There's currently only one type of JavaScript visualization.