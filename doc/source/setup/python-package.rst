.. include:: ../_resources.rst

.. _setup-python-package:

################################
Install Python package from PyPI
################################


************
Introduction
************

Kotori can be installed in different variants.

Setting up Kotori as Python package is suitable for installing on platforms
where there is no native distribution package available yet.

We recommend to either use the ``pip install --user`` option in order not to
clutter your distribution Python or use a virtualenv_. In this manner, your
installation will not require root permissions and the Python libraries of
your system distribution will stay completely untouched.

When aiming to work on the source code of Kotori, we recommend to read the
documentation about how to :ref:`kotori-sandbox`.


.. _setup-python-package-cpython:

***********************
Installation on CPython
***********************


Prerequisites
=============

Installing Kotori using a Python package might need development tools properly
installed::

    apt install build-essential python3-dev python3-pip libffi-dev libssl-dev


From PyPI
=========

Kotori releases are published to https://pypi.org/project/kotori/ ::

    # Set option to make the pip installer prefer binary dependencies
    # This might prevent compilation steps for some of them
    export PIP_PREFER_BINARY=1

    # Install latest Kotori release with extra features "daq" and "export"
    pip install --user kotori[daq,export]

    # Install more extra features
    pip install --user kotori[daq,daq_geospatial,export,plotting,scientific,firmware]

    # Install particular version
    pip install --user kotori[daq,export]==0.26.6


From git repository
===================
::

    pip install --user --prefer-binary --editable git+https://github.com/daq-tools/kotori.git#egg=kotori[daq]

.. seealso:: https://pip.pypa.io/en/stable/cli/pip_install/


.. _setup-python-virtualenv:

Using virtualenv
================

::

    # Create virtualenv
    python3 -m venv .venv

    # Activate virtualenv
    source .venv/bin/activate

    # Install package
    pip install kotori



.. _run-on-pypy:
.. _setup-python-package-pypy:

********************
Installation on PyPy
********************


Prerequisites
=============
::

    brew install pypy3 openblas lapack


Using virtualenv
================
::

    pypy3 -m venv .venvpypy
    source .venvpypy/bin/activate

    export OPENBLAS="$(brew --prefix openblas)"
    export LAPACK="$(brew --prefix lapack)"
    pip install --prefer-binary --no-binary=numpy kotori[daq,export]
