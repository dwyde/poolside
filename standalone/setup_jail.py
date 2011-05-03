import os
import pwd
import grp

#import http_server

NEW_USER = 'nobody'
NEW_GROUP = 'nobody'
NEW_ROOT = 'jail'

def jail_dir(new_root):
    current_dir = os.path.abspath(os.getcwd())
    return os.path.join(current_dir, new_root)

def setup_jail():
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
    print 'Working directory: %s\nUser id: %d\nGroup id: %d' % \
              (os.getcwd(), os.getuid(), os.getgid())

    # Run the server
    http_server.main()
    
