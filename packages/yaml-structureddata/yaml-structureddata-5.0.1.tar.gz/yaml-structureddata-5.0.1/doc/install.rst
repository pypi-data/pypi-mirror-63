Installing StructuredData
=========================

Parts of StructuredData
-----------------------

StructuredData consists of scripts, python modules and documentation files.

StructuredData is available as tar.gz or zip file and on pypi. The sections
below describe all installation options.

Requirements
------------

StructuredData requires at least `Python <https://www.python.org>`_ version 3.2.3 or newer.

StructuredData is tested on `debian <https://www.debian.org>`_ and 
`Fedora <https://getfedora.org>`_ linux distributions but should run on all
linux distributions. It probably also runs on other flavours of unix, probably
even MacOS, but this is not tested.

It may run on windows, escpecially the `Cygwin <https://www.cygwin.com>`_
environment, but this is also not tested.

Install from pypi with pip
--------------------------

In order to install StructuredData with `pip <https://en.wikipedia.org/wiki/Pip_(package_manager)>`_, 
you use the command [1]_::

  pip install YAML-StructuredData

.. [1] You may have to use ``pip3`` or ``pip-3.2`` or a similar command instead of ``pip`` on your system to use python 3.

You find documentation for the usage of pip at `Installing Python Modules
<https://docs.python.org/3/installing/index.html#installing-index>`_.

Install from source (tar.gz or zip file)
----------------------------------------

Download the file from here:

* `YAML-StructuredData downloads at Sourceforge <https://sourceforge.net/projects/yaml-structureddata/files/?source=navbar>`_

unpack the tar.gz file with::

  tar -xzf <PACKAGENAME>

or unpack the zip file with::

  unzip <PACKAGENAME>

The StructuredData distribution contains the install script "setup.py". If you install
StructuredData from source you always invoke this script with some command line options. 

The following chapters are just *examples* how you could install StructuredData. For a
complete list of all possibilities see 
`<https://docs.python.org/3/installing/index.html#installing-index>`_.

Install with::

  python3 setup.py [options]

Whenever ``python`` is mentioned in a command line in the following text remember
that you may have to use ``python3`` instead.

Install as root to default directories
::::::::::::::::::::::::::::::::::::::

This method will install StructuredData on your systems default python library and
binary directories.

Advantages:

- You don't have to modify environment variables in order to use StructuredData.
- All users on your machine can easily use StructuredData.

Disadvantages:

- You must have root or administrator permissions to install StructuredData.
- Files of StructuredData are mixed with other files from your system in the same
  directories making it harder to uninstall StructuredData.

For installing StructuredData this way, as user "root" enter::

  python setup.py install

Install to a separate directory
:::::::::::::::::::::::::::::::

In this case all files of StructuredData will be installed to a separate directory.

Advantages:

- All StructuredData files are below a directory you specify, making it easy to uninstall
  StructuredData.
- If you have write access that the directory, you don't need root or
  administrator permissions.

Disadvantages:

- Each user on your machine who wants to use StructuredData must have the correct
  settings of the environment variables PATH and PYTHONPATH.

For installing StructuredData this way, enter::

  python setup.py install --prefix <DIR>

where <DIR> is your install directory.

In order to use StructuredData, you have to change the environment variables PATH and
PYTHONPATH. Here is an example how you could do this::

  export PATH=<DIR>/bin:$PATH
  export PYTHONPATH=<DIR>/lib/python<X.Y>/site-packages:$PYTHONPATH

where <DIR> is your install directory and <X.Y> is your python version number.
You get your python version with this command::

  python -c 'from sys import *;stdout.write("%s.%s\n"%version_info[:2])'

You may want to add the environment settings ("export...") to your shell setup,
e.g. $HOME/.bashrc or, if your are the system administrator, to the global
shell setup.

Install in your home
::::::::::::::::::::

In this case all files of StructuredData are installed in a directory in your home called
"StructuredData".

Advantages:

- All StructuredData files are below $HOME/StructuredData, making it easy to uninstall StructuredData.
- You don't need root or administrator permissions.

Disadvantages:

- Only you can use this installation.
- You need the correct settings of environment variables PATH and
  PYTHONPATH.

For installing StructuredData this way, enter::

  python setup.py install --home $HOME/StructuredData

You must set your environment like this::

  export PATH=$HOME/StructuredData/bin:$PATH
  export PYTHONPATH=$HOME/StructuredData/lib/python:$PYTHONPATH

You may want to add these lines to your shell setup, e.g. $HOME/.bashrc.

