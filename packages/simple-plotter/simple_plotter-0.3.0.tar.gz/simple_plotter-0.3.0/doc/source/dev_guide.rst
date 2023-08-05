.. _dev_guide:

Contributing
============

If you would like to contribute to the project feel free to fork the project and raise a merge request on gitlab.

Find some development related remarks below:

Concept
-------

*simple_plotter* is primarily a very specific python-code generator - i.e. the parameters provided by the GUI front-end
will be used to generate a python script, which is then executed to generate the plot.

The scripts will be created based on jinja2 templates - see simple_plotter/core/templates.

Some code checking is done using the ast_ module to provide basic security (e.g. prevent unwanted commands or imports).
See the CodeChecker class in the code_parser module.

Package versions
----------------

setuptools_scm_ is used to fetch the version strings from git tags/commits automatically.

Building conda packages
-----------------------

There will probably be no need to update the meta.yaml manually.
conda-build's jinja templating functionality is used in meta.yaml to fetch the package information from setup.py (except
for the package version).

Since setuptools_scm is used, there is no version argument, that can be imported with the load_setup_py_data function
in meta.yaml.

Therefore **conda packages should be built using the build_conda_package.sh shell script.**

This script first reads the (auto-generated) version from setup.py and passes it to an environment variable, which is
used in the meta.yaml.

.. note::

    Unfortunately there is currently no kivy-garden.graph package for conda. So conda packages will miss this
    dependency! You will have to install kivy-garden.graph via pip.

Testing
-------

gitlab CI/CD will run the test functions (pytest) - see tests/ on each commit and update the `code coverage report`_.
Tests are currently only defined for the simple_plotter.core modules (not for the GUI).

Project documentation
---------------------

Documentation sources for sphinx are stored in the doc/ folder.
To build the documentation you need *sphinx* and the *sphinx-rtd-theme* package installed.

When commits to master are pushed to the gitlab repository the documentation is automatically generated on readthedocs:

https://simple-plotter.readthedocs.io/latest

If tags are pushed documentation will be generated for

https://simple-plotter.readthedocs.io/stable

.. _ast: https://docs.python.org/3/library/ast.html
.. _code coverage report: https://thecker.gitlab.io/simple-plotter/index.html
.. _setuptools_scm: https://github.com/pypa/setuptools_scm