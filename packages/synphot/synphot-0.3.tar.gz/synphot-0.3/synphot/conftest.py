import os

try:
    from pytest_astropy_header.display import PYTEST_HEADER_MODULES, TESTED_VERSIONS
except ImportError:
    PYTEST_HEADER_MODULES = {}

try:
    from .version import version
except ImportError:
    version = 'unknown'

# Uncomment the following line to treat all DeprecationWarnings as
# exceptions
from astropy.tests.helper import enable_deprecations_as_exceptions
enable_deprecations_as_exceptions()

# Uncomment and customize the following lines to add/remove entries
# from the list of packages for which version numbers are displayed
# when running the tests.
PYTEST_HEADER_MODULES['Astropy'] = 'astropy'
PYTEST_HEADER_MODULES['specutils'] = 'specutils'
PYTEST_HEADER_MODULES.pop('Matplotlib')
PYTEST_HEADER_MODULES.pop('Pandas')
PYTEST_HEADER_MODULES.pop('h5py')

packagename = os.path.basename(os.path.dirname(__file__))
TESTED_VERSIONS[packagename] = version
