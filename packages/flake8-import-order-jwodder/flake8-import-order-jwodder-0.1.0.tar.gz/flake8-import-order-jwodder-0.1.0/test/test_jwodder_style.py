import ast
import os
from   os.path                     import dirname, join
import re
from   flake8_import_order.checker import ImportOrderChecker
from   flake8_import_order.styles  import lookup_entry_point
import pytest

DATA_DIR = join(dirname(__file__), 'data')

ERROR_RGX = re.compile("# ((?:I[0-9]{3} ?)+) ?.*$")

style_entry_point = lookup_entry_point('jwodder')

options = {
    'application_import_names': [
        'flake8_import_order', 'namespace.package_b', 'tests',
    ],
    'application_package_names': ['localpackage'],
    'import_order_style': style_entry_point,
}

@pytest.mark.parametrize('pyfile', os.listdir(DATA_DIR))
def test_jwodder_style(pyfile):
    pypath = join(DATA_DIR, pyfile)
    with open(pypath) as fp:
        data = fp.read()
    expected = []
    for line in data.splitlines():
        m = ERROR_RGX.search(line)
        if m:
            expected.extend(m.group(1).split())
    tree = ast.parse(data, pypath)
    checker = ImportOrderChecker(pypath, tree)
    checker.options = options
    codes = [error.code for error in checker.check_order()]
    assert codes == expected
