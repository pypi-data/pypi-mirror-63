Getting started
===============

This chapter will give a basic instructions for installing and running the program.
For detailed usage instructions please see the :ref:`userguide`.

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

The Android app is available in the F-Droid_ app-store [work in progress...].

Alternatively you can build the Android APK from source. Follow the instructions
on https://gitlab.com/thecker/simple-plotter4a

.. note::

    Due to a broken matplotlib recipe in the *python-for-android* project only the *kivy-garden-graph* configuration is
    working on Android - see `Configuration options`_.


Configuration options
---------------------

The table below shows the currently available configuration options.

+---------------------------+------------------------------------+------------------+-------------------------------+
|      Configuration        |              plotting library      |  GUI frame work  |                               |
|                           +--------------+---------------------+---------+--------+                               |
|                           |  matplotlib  |  garden.graph       |   PyQt  |  kivy  |     Package                   |
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

If you would like to contribute see :ref:`dev_guide`.

.. _F-Droid: https://f-droid.org/en/
