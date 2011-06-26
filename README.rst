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
resource limits. If you don't use the chroot jail, all security bets are off.
 
Warning: notebooks can access any kernel, but the client-side permissions
should work properly.

You should configure CouchDB 1.1.0 to use SSL. Otherwise,
plain text passwords and authentication cookies will be transmitted over
the network.

The evaluation server checks CouchDB cookies via HTTP. I haven't figured 
out a way to make `openssl` work in the chroot jail. I'm having issues 
with /dev/urandom, and possibly other things.

Dependencies
------------
To run this software, you will need the following packages:
    
  - `Python <http://python.org>`_ 2.7
  - `CouchDB <http://couchdb.apache.org>`_ 1.1.0
  - `CouchApp <http://couchapp.org>`_
  - `Ruby <http://www.ruby-lang.org/en/>`_ >= 1.9.1 (to make Ruby kernels work)

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
address. This should be configured in CouchDB's ``local.ini`` file ::

  [httpd_global_handlers]
  _eval = {couch_httpd_proxy, handle_proxy_req, <<"http://localhost:8283">>}

where ``http://localhost:8283`` can be replaced by the address at which
your evaluation server is running.

Running the Standalone Server
-----------------------------
Example call ::

  cd poolside/standalone
  sudo python run_server -p 8283 -c http://localhost:5984 -j

or, to skip CouchDB authentication and the chroot jail ::
  
  python run_server.py

You need to be root in order to create the chroot jail, but the server
process drops privileges immediately after doing so.

Command Line Arguments
~~~~~~~~~~~~~~~~~~~~~~

-c couch_server              URL of a CouchDB server to use for
                             authentication. If absent, all well-formed
                             requests will be accepted.
-p port	                     Port on which the evaluation server will listen.
-j jail                      Use a chroot jail (requires root privileges).

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
