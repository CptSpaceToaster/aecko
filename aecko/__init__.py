"""Package for aecko"""
# System
import sys

__project__ = 'Aecko'
__version__ = '1.0.0rc3'

CLI = 'aecko'
VERSION = '{0} v{1}'.format(__project__, __version__)
DESCRIPTION = 'Generate representative image differences in a directory'

MIN_PYTHON_VERSION = 3, 3

if not sys.version_info >= MIN_PYTHON_VERSION:
    exit("Python {}.{}+ is required.".format(*MIN_PYTHON_VERSION))

# Local
try:
    # from thing import foo
    pass
except ImportError:
    pass
