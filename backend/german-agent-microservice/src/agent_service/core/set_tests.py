import os
import sys, os

def set_path():
    testdir = os.path.dirname(__file__)
    sys.path.insert(0, os.path.abspath(os.path.join(testdir, '../../../')))
