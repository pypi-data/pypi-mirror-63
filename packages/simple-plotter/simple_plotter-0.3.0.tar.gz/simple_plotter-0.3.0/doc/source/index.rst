.. simple_plotter documentation master file, created by
   sphinx-quickstart on Sun Oct 13 17:18:15 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to simple_plotter's documentation!
==========================================

simple_plotter is a code-generator and minimal GUI frontend for plotting functional 2D x,y-plots.
The function equation has to be entered in python syntax (allowing the use of numpy statements).

Besides saving and loading projects to/from a JSON file, simple_plotter also provides the possibility to export the
project as python code.

The *simple_plotter* package comes with a Qt-based GUI-frontend. There is an additional alternative kivy-based frontend,
created primarily for the Android port - simple-plotter4a_ - which can also be used on the desktop (see screen shots
below).

simple_plotter is released under GPLv3+, Copyright (c) 2019-2020 Thies Hecker

It contains a color map definition taken from the matplotlib project, Copyright (c) 2012-2020 Matplotlib Development
Team; All Rights Reserved

For details on licenses see :ref:`licenses` or the NOTICE and LICENSE files in the `source code repository`_.

.. figure:: screen_shot_qt.png

   Screen shot of the Qt-based GUI

.. figure:: screen_shot_android.png

   Screen shot of the kivy-based GUI (running on Android)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   howto.rst
   user_guide.rst
   license.rst
   dev_guide.rst
   api.rst
   roadmap.rst
   changelog.rst



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _simple-plotter4a: https://gitlab.com/thecker/simple-plotter4a
.. _source code repository: https://gitlab.com/thecker/simple-plotter