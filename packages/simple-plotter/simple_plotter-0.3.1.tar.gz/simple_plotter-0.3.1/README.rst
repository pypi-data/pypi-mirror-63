.. image:: https://readthedocs.org/projects/simple-plotter/badge/?version=latest
    :target: https://simple-plotter.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://gitlab.com/thecker/simple-plotter/badges/master/pipeline.svg
    :target: https://gitlab.com/thecker/simple-plotter/commits/master
    :alt: pipeline status

.. image:: https://gitlab.com/thecker/simple-plotter/badges/master/coverage.svg?job=test
    :target: https://thecker.gitlab.io/simple-plotter/index.html
    :alt: Code coverage report for core modules

simple-plotter
==============

simple_plotter is a code-generator and minimal GUI frontend for plotting functional 2D x,y-plots.
The function equation has to be entered in python syntax (allowing the use of numpy statements).

Besides saving and loading projects to/from a JSON file, simple_plotter also provides the possibility to export the
project as python code.

The *simple_plotter* package comes with a Qt-based GUI-frontend. There is an additional alternative kivy-based frontend,
created primarily for the Android port - simple-plotter4a_ - which can also be used on the desktop.

simple_plotter is released under GPLv3+, Copyright (c) 2019-2020 Thies Hecker

It contains a color map definition taken from the matplotlib project, Copyright (c) 2012-2020 Matplotlib Development
Team; All Rights Reserved

See NOTICE and LICENSE files for details on licensing.

Getting started
===============

Desktop
-------

As *simple_plotter* is entirely written in python it should run on any desktop platform with a python3
interpreter and support for the required packages (see `Requirements`_).

The packages for *simple-plotter* are available on PyPI. The easiest solution is to install the base package with the
default GUI front-end and plotting library (i.e. PyQt and matplotlib) using *pip*.

Open up a terminal and type:

::

    pip install simple-plotter[Qt-matplotlib]

It will automatically install the requirements.

To launch simple-plotter just enter:

::

    simple-plotter

To install different GUI/plotting library options see `Configuration options`_.


Android
-------

The Android app is available in the F-Droid_ app-store.

If you would like to build the Android APK from source follow the instructions
on https://gitlab.com/thecker/simple-plotter4a

.. note::

    Due to a broken matplotlib recipe in the *python-for-android* project only the *kivy-garden-graph* configuration is
    working on Android - see `Configuration options`_.


Configuration options
---------------------

The table below shows the currently available configuration options.

+---------------------------+------------------------------------+------------------+-------------------------------+
|                           |              plotting library      |  GUI frame work  |                               |
+---------------------------+--------------+---------------------+---------+--------+-------------------------------+
|       Configuration       |  matplotlib  |  garden.graph       |   PyQt  |  kivy  |     Package                   |
+===========================+==============+=====================+=========+========+===============================+
|     Qt-matplotlib         |      x       |                     |    x    |        | simple-plotter                |
+---------------------------+--------------+---------------------+---------+--------+-------------------------------+
|     kivy-matplotlib       |      x       |                     |         |   x    | simple-plotter4a              |
+---------------------------+--------------+---------------------+---------+--------+-------------------------------+
|     kivy-garden-graph     |              |          x          |         |   x    | simple-plotter4a              |
+---------------------------+--------------+---------------------+---------+--------+-------------------------------+

Use ``pip install <Package>[<Configuration>]`` to install one of the configuration options - e.g.:

::

    pip install simple-plotter4a[kivy-matplotlib]

Similarly you launch the programs with ``simple-plotter-<Configuration>`` - e.g.:

::

    simple-plotter-kivy-matplotlib


Requirements
------------

*simple_plotter* is written in python3 and requires has following dependencies:

Mandatory:

* jsonpickle
* numpy
* setuptools_scm
* jinja2

Optional:

* pyqt >= 5
* matplotlib>=2
* kivy>=1.11
* kivy-garden.graph>=0.4

The optional dependencies provide are related to the different `Configuration options`_.

Source code
-----------

The source code can be obtained from:

https://gitlab.com/thecker/simple-plotter

and (for the kivy-based GUI)

https://gitlab.com/thecker/simple-plotter4a

.. _F-Droid: https://f-droid.org/en/
.. _simple-plotter4a: https://gitlab.com/thecker/simple-plotter4a