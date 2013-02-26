
import sys

class VersionError(Exception): pass


def is_py3():
    return sys.version_info[0] == 3
    
def require_py3():
    """ Assert whether the current module is being run under Python3. """
    if not is_py3():
        raise VersionError("requires Python 3")
