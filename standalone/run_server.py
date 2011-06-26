#!/usr/bin/env python
# 
# This file is part of Poolside, a computational notebook.
# Copyright (C) 2011 David Wyde and Chris Hart, New College of Florida
#
# Poolside is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 
# 02110-1301, USA.

"""
Run a Python and Ruby code evaluation server, possibly in a chroot jail.
"""

import argparse
import os
import pwd
import grp

from eval_server import EvalServer, EvalHandler, CouchAuthHandler
from config import (DEFAULT_PORT, JAIL_ROOT, JAIL_USER, JAIL_GROUP,
                   KERNEL_DIR)

def read_arguments():
    """Process command line arguments."""
    
    parser = argparse.ArgumentParser(description='An HTTP server to run code')
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT,
                       help='port on which the server will run')
    parser.add_argument('-c', '--couch', dest='couch', default=None,
                       help='address at which CouchDB is running')
    parser.add_argument('-j', '--jail', action='store_true',
                        help='use a chroot jail (requires root privileges)')
    args = parser.parse_args()
    return args

def setup_jail():
    """Create and enter the chroot jail."""
    
    # Choose a new user, group, and root directory.
    new_uid = pwd.getpwnam(JAIL_USER)[2]
    new_gid = grp.getgrnam(JAIL_GROUP)[2]
    root_dir = os.path.join(os.path.abspath(os.getcwd()), JAIL_ROOT)

    # Set up the jail.
    os.chdir(root_dir)
    os.chroot(root_dir)
    os.setgid(new_gid)
    os.setuid(new_uid)

def main():
    """
    Main function: create and run an `EvalServer`.
    
    Authenticate against a CouchDB server, if one is supplied.
    Use a chroot jail if the appropriate flag is specified.
    """
    
    args = read_arguments()
    
    # Set up server
    address = ('127.0.0.1', args.port)
    if args.couch:
        server = EvalServer(address, CouchAuthHandler)
        server.set_couch_server(args.couch)
    else:
        server = EvalServer(address, EvalHandler)
    
    # Possibly set up chroot jail (as specified in the "config.py" file)
    if args.jail:
        setup_jail()
        server.set_kernel_dir(KERNEL_DIR)
    else:
        server.set_kernel_dir(os.path.join(JAIL_ROOT, KERNEL_DIR))
    
    print 'Ready to serve at ', server.server_address
    server.serve_forever()

if __name__ == '__main__':
    main()
