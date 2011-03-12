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

  I'll get to chroot jails and something like *setrlimit* in the near future.

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

* ``-p`` : Port on which the *eval server* will run.  Defaults to 8282.

An Aside About Configuration

* In an earlier implementation, I set the server port in a field on the _design
  doc. I think this is a good way to share between the CouchApp and the HTTP
  server, and I'll probably go back to it soon.
  
* The CouchDB port should also be a command line arg to the HTTP server. It was,
  but for some reason it isn't right now.

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

Pressing "enter" in the textarea is broken -- just click the buttons.

The "cell types" aren't yet fully implemented. CouchDB doesn't persist the
type of cell.

CORS seems to get confused by HTTP cookies. This makes it hard
to authenticate with CouchDB. Might look at JSON-P, or just wait for CouchDB
1.1.0 and see if that fixes the cross-domain problem ("external process"
improvements).
