"""Set up a chroot jail, through Python."""

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
