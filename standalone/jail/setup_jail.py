import os
import pwd

NEW_USER = 'nobody'
NEW_ROOT = 'new_root'

def jail_dir(new_root):
    current_dir = os.path.abspath(os.getcwd())
    return os.path.join(current_dir, new_root)

def setup_jail():
    new_uid = pwd.getpwnam(NEW_USER)[2]
    root_dir = jail_dir(NEW_ROOT)
    
    print 'uid:  %s\nroot: %s' % (new_uid, root_dir)

    os.chdir(root_dir)
    os.chroot(root_dir)
    os.setuid(new_uid)

    #os.environ['PATH'] = '/usr/bin'

    del new_uid
    del root_dir

def try_stuff():
    #os.chdir('/etc')
    #Popen(['cd', '..'])
    #Popen(['python', ]
    #import sys
    #print sys.path
    
    import os
    print os.system('ls')
    print os.environ
    
    import sys
    print sys.path
    #import math
    #print math.sqrt(10)

if __name__ == '__main__':
    setup_jail()

    try_stuff()
