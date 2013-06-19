Pandas and Friends
------------------

Pandas - Python Data Analysis Library
+++++++++++++++++++++++++++++++++++++

* Austin Godber
* Mail: godber@uberhip.com
* Twitter: @godber
* Source: http://github.com/desertpy/presentations

.. raw:: pdf

  PageBreak oneColumn

What does it do?
----------------

Pandas is a Python data analysis tool built on top of NumPy that provides a
suite of data structures and data manipulation functions to work on those data
structures.  It is particularly well suited for working with time series data.

Getting Started
---------------

Installing with pip or apt-get::

  pip install pandas
  # or
  sudo apt-get install python-pandas

Dependencies, required, recommended and optional::

  # Required
  numpy, python-dateutil, pytx
  # Recommended
  numexpr, bottleneck
  # Optional
  cython, scipy, pytables, matplotlib, statsmodels, openpyxl

Background - IPython
--------------------

IPython is a fancy python console.  Try running ``ipython`` on your command
line.  Some IPython tips::

  # Special commands, 'magic functions', begin with %
  %quickref, %who, %run, %reset
  # Shell Commands
  ls, cd, pwd, mkdir
  help(), help(obj)
  # Tab completion of variables, attributes and methods

There is a web interface to IPython, known as the IPython notebook, start it
like this::

  ipython notebook

Background - NumPy
------------------


Data Structures
----------------



* Series - 1D labeled array
* DataFrame - 2D labeled array
* Panel - 3D labeled array (More D)


Series
------


DataFrame
---------


Panel
-----



Plotting
--------


References
----------

* `virtualenv <http://virtualenv.openplans.org/>`_
* `virtualenvwrapper <http://www.doughellmann.com/projects/virtualenvwrapper/>`_
* `P5M1 Orbital Image <http://en.wikipedia.org/wiki/File:P5M1.png>`_
* Presentation Source - http://github.com/godber/ATOM

.. header::

        ATOM: Virtualenv

.. footer::

        © Austin Godber (@godber), 2013
