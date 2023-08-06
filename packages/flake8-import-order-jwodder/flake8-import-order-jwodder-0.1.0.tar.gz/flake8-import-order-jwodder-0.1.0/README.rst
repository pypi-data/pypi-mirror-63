.. image:: http://www.repostatus.org/badges/latest/active.svg
    :target: http://www.repostatus.org/#active
    :alt: Project Status: Active — The project has reached a stable, usable
          state and is being actively developed.

.. image:: https://travis-ci.com/jwodder/flake8-import-order-jwodder.svg?branch=master
    :target: https://travis-ci.com/jwodder/flake8-import-order-jwodder

.. image:: https://codecov.io/gh/jwodder/flake8-import-order-jwodder/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jwodder/flake8-import-order-jwodder

.. image:: https://img.shields.io/pypi/pyversions/flake8-import-order-jwodder.svg
    :target: https://pypi.org/project/flake8-import-order-jwodder/

.. image:: https://img.shields.io/github/license/jwodder/flake8-import-order-jwodder.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
    :target: https://saythanks.io/to/jwodder

`GitHub <https://github.com/jwodder/flake8-import-order-jwodder>`_
| `PyPI <https://pypi.org/project/flake8-import-order-jwodder/>`_
| `Issues <https://github.com/jwodder/flake8-import-order-jwodder/issues>`_

``flake8-import-order-jwodder`` defines an import order style ``jwodder`` for
use with `flake8-import-order
<https://pypi.org/project/flake8-import-order/>`_.  The ``jwodder`` style is
the same as the ``appnexus`` style bundled with ``flake8-import-order``, except
that names in ``from X import ...`` lines are sorted case-sensitively.

Installation
============
Just use `pip <https://pip.pypa.io>`_ (You have pip, right?) to install
``flake8-import-order-jwodder`` and its dependencies::

    pip install flake8-import-order-jwodder


Example
=======
An example of imports sorted according to the ``jwodder`` style::

    from __future__ import absolute_import

    import ast
    from functools import *
    import os
    from os import path
    import StringIO
    import sys

    import X
    from X import *
    from X import A
    from X import B, C, b, d
    import Y
    from Y import *
    from Y import A
    from Y import B, C, D
    from Y import e
    import Z
    from Z import A
    from Z.A import A
    from Z.A.B import A

    from localpackage import A, b

    import flake8_import_order
    from flake8_import_order import *
    from . import A
    from . import B
    from .A import A
    from .B import B
    from .. import A
    from .. import B
    from ..A import A
    from ..B import B
