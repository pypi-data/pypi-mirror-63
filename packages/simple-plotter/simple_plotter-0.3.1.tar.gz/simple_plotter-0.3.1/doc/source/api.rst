.. _apiRef:

API reference
=============

This section describes the API of the backend - i.e. the **code_generator** and **code_parser** module.


code_generator
--------------

The module consists of a class `DataHandler`_ which includes the code generator methods and
some data container classes (`Formula`_ and `PlotData`_).

.. autofunction:: simple_plotter.core.code_generator.check_valid_input

Formula
~~~~~~~

.. autoclass:: simple_plotter.core.code_generator.Formula
    :members:

PlotData
~~~~~~~~

.. autoclass:: simple_plotter.core.code_generator.PlotData
    :members:

DataHandler
~~~~~~~~~~~

.. autoclass:: simple_plotter.core.code_generator.DataHandler
    :members:


code_parser
-----------

This module consist of a data container class `Code`_ and the `CodeChecker`_ class, which uses *ast* to analyze code
elements and identify unwanted code.

Code
~~~~

.. autoclass:: simple_plotter.core.code_parser.Code
    :members:

CodeChecker
~~~~~~~~~~~

.. autoclass:: simple_plotter.core.code_parser.CodeChecker
    :members:


advanced_graph
--------------

This module includes a class `AnnotatedLinePlot`_ which is a specialized extension of the kivy-garden.graph package.
The *AnnotatedLinePlot* adds some matplotlib-like behavior (e.g. automatic axis-scaling, a legend, plot title) to the
garden.graph *LinePlot* class.

AnnotatedLinePlot
~~~~~~~~~~~~~~~~~

.. autoclass:: simple_plotter.core.advanced_graph.AnnotatedLinePlot
    :members:
