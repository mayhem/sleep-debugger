import os
import sys
from atexit import register

class ProcessLock(object):

    def __init__(self, lockfile):

        self.lockfile = lockfile

    def allowed_to_start(self):

        if not os.path.exists(self.lockfile):
            return True

        try:
            f = open(self.lockfile, "r")
            pid = int(f.read())
            f.close()
        except Exception:
            return True

        print "Found lockfile owned by process %d." % pid
        try:
            os.kill(pid, 0)
        except OSError:
            os.unlink(self.lockfile)
            print "... which is not running anymore. Removing lockfile."
            return True

        print "... which is still running. Not starting."
        return False


    def create(self):
        if not self.lockfile:
            return

        if os.path.exists(self.lockfile):
            print "Lock file %s exists, aborting." % self.lockfile
            sys.exit(-1)

        # Register a cleanup handler
        register(lambda: self.cleanup())

        # Create a lockfile
        try:
            f = open(self.lockfile, "w")
        except IOError as e:
            print "Cannot create lock file %s: %s" % (self.lockfile, e)
            sys.exit(-2)

        f.write("%d" % os.getpid())
        f.close()


    def cleanup(self):
        # Remove the lock file
        try:
            os.unlink(self.lockfile)
        except OSError:
            pass
