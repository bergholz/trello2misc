''' utils.py
Python helper methods.
'''

import os, configparser

# Returns the real directory name for a given file name.
# Resolves symbolic links, for example.
def realdirname(file):
    path = os.path.realpath(__file__)
    dirname = path[:path.rindex(os.sep)]
    return dirname

# Returns a configuration object from a given configuration file 
# located in the current directory.
def readconfig(inifile):
    config = configparser.ConfigParser()
    config.read(realdirname(__file__) + os.sep + inifile)
    return config

# Turns none into empty string, e.g. to enable sorting.
def nonetoempty(string):
    if not string:
        return ""
    return string

# Turns string.strip() operation into a function.
def strip(string):
    return string.strip()
