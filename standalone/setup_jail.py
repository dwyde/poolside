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
Set up a chroot jail, through Python.
"""

import os
import pwd
import grp

from eval_server import main

NEW_USER = 'nobody'
NEW_GROUP = 'nogroup' # 'nobody'
NEW_ROOT = 'jail'

def jail_dir(new_root):
    """Determine the directory in which to create a chroot jail."""
    
    current_dir = os.path.abspath(os.getcwd())
    return os.path.join(current_dir, new_root)

def setup_jail():
    """Create and enter the chroot jail."""
    
    # Choose a new user, group, and root directory.
    new_uid = pwd.getpwnam(NEW_USER)[2]
    new_gid = grp.getgrnam(NEW_GROUP)[2]
    root_dir = jail_dir(NEW_ROOT)

    # Set up the jail.
    os.chdir(root_dir)
    os.chroot(root_dir)
    os.setgid(new_gid)
    os.setuid(new_uid)

if __name__ == '__main__':
    setup_jail()
    main()
