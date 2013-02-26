

from __future__ import absolute_import
import sys

from .file_id_iter import file_id_iter
from .py3 import require_py3, is_py3

if not is_py3():
    # Python3 is unicode compatible by default
    from .unicodecsvwriter import UnicodeWriter