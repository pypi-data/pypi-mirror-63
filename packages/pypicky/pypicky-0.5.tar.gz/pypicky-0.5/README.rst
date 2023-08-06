About PyPIcky
=============

PyPIcky is a tiny package that provides a proxy to the PyPI server but with
version requirements pre-applied.

Installing
----------

To install::

    pip install pypicky

Using
-----

Once installed, create a
`requirements file <https://pip.readthedocs.io/en/1.1/requirements.html>`_
(using the same syntax that you would normally use for pip) and then start up
PyPIcky by using the ``pypicky`` command and passing it the name of the
requirements file as a command-line argument::

    pypicky requirements.txt

This will start up a small web server, and will print out a line such as::

    Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

You can then call pip with::

    pip install --index-url http://127.0.0.1:5000/ astropy

and this will then install the requested packages and all dependencies, ignoring
packages excluded by the requirements file.

This can then be used for example with other tools that support PyPI index URLs,
such as `tox <https://tox.readthedocs.io/en/latest/>`_.

Caveats/warnings
----------------

If a package is already installed, pip will not try installing it again. This
means that if e.g. you try and run pip as described above, but the package you
are trying to install (or any of its dependencies) is already installed, no
matter how recent the version, it will not be installed again. Therefore, I
recommend using pip with the custom index URL inside a clean environment (but
you can run the pypicky command inside your regular environment.)
