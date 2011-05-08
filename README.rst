Poolside
========

Introduction
------------
`Poolside` is a computational notebook system.  It is designed for data
analysis and visualization.

This software uses CouchDB as both a storage backend and a web server.
A standalone Python HTTP server executes code and returns results, via AJAX.

Security Notes
--------------
The current security features on the evaluation server are chroot jails and 
resource limits.
 
Warning: notebooks can access any kernel, but the client-side permissions
should work properly.

Nginx should be used to allow SSL connections to CouchDB. Otherwise,
plain text passwords and authentication cookies will be transmitted over
the network.

The evaluation server checks CouchDB cookies via HTTP. I haven't figured 
out a way to make `openssl` work in the chroot jail. I'm having issues 
with /dev/urandom, and possibly other things.

Dependencies
------------
To run this software, you will need the following packages:
    
  - `Python <http://python.org>`_ 2.6 or 2.7
  - `CouchDB <http://couchdb.apache.org>`_ >= 1.0.1
  - `CouchApp <http://couchapp.org>`_
  - `Ruby <http://www.ruby-lang.org/en/>`_ >= 1.9.1 (to make Ruby kernels work)
  - `nginx <http://nginx.org/>`_ Tested with 1.0.1 (for SSL).

Installation into CouchDB
-------------------------
Use CouchApp to initialize and update the files stored in CouchDB ::

  cd poolside/notebook
  couchapp push http://localhost:5984/database

or :: 

  couchapp push 'http://admin:password@localhost:5984/database'

Server Configuration
--------------------
The JavaScript notebook frontend (in CouchDB) needs to know the eval server's
address. This is stored in an attachment to the design document ::

  poolside/notebook/eval_server.json

Running the Standalone Server
-----------------------------
Example call ::

  cd poolside/standalone
  python http_server.py -p 8283 -c http://localhost:5984

Command Line Arguments

-c couch_server        URL of the CouchDB server.
-p port	               Port on which the evaluation server will listen.

Accessing Notebooks
-------------------
Finally, access the following URL in your JavaScript-enabled web browser ::

  http://localhost:5984/database/_design/notebook/_rewrite/poolside/test

The last part of the URL (i.e., "test") is the name of notebook. 
Change it to create new notebooks.

Random Points
-------------
This project has had a number of different architectures, so its documentation
may lag behind the actual code.

There's currently only one type of JavaScript visualization.

A sample `nginx` configuration, tested with version 1.0.1, is at
``poolside/conf/nginx.conf``.
