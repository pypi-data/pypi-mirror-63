pippurge
==========

Enhancement for pip uninstall command, that it removes all dependencies of an uninstalled package.

Quickstart
------------

Uninstall package, e.g, flask:

::

    $ pippurge flask -y

Uninstall multiple packages, e.g, flask, requests:

::

    $ pippurge flask requests -y

Installation
--------------

You can install "pippurge" via pip from `PyPI <https://pypi.python.org/pypi/pippurge>`_:

::

    $ pip install pippurge
	
Usage
-------

::

    $ pippurge --help
    usage: pippurge [-h] [-y] packages [packages ...]

    Uninstall packages with all its dependencies.

    positional arguments:
      packages    some packages

    optional arguments:
      -h, --help  show this help message and exit
      -y, --yes   don't ask for confirmation of uninstall deletions.
