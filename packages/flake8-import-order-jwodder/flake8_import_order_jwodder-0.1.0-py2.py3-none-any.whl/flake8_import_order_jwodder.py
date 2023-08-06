"""
Yet another import order style

``flake8-import-order-jwodder`` defines an import order style ``jwodder`` for
use with flake8-import-order <https://pypi.org/project/flake8-import-order/>.
The ``jwodder`` style is the same as the ``appnexus`` style bundled with
``flake8-import-order``, except that names in ``from X import ...`` lines are
sorted case-sensitively.

Visit <https://github.com/jwodder/flake8-import-order-jwodder> for more
information.
"""

__version__      = '0.1.0'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'flake8-import-order-jwodder@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/flake8-import-order-jwodder'

from flake8_import_order.styles import AppNexus, Google

class JWodder(AppNexus):
    @staticmethod
    def sorted_names(names):
        return sorted(names)

    @staticmethod
    def import_key(import_):
        modules = [Google.name_key(module) for module in import_.modules]
        return (import_.type, import_.level, modules, import_.names)
