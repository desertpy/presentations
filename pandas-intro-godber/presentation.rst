Pandas and Friends
------------------

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

Getting Started - Installation
------------------------------

Installing with pip or apt-get::

  pip install pandas
  # or
  sudo apt-get install python-pandas

* Mac - Homebrew or MacPorts to get the dependencies, then pip
* Windows - Python(x,y)?
* Commercial Pythons


Panda's Friends!
----------------

.. image:: panda-on-a-unicorn.jpg


Getting Started - Dependencies
------------------------------

Dependencies, required, recommended and optional

.. code-block:: bash

  # Required
  numpy, python-dateutil, pytx
  # Recommended
  numexpr, bottleneck
  # Optional
  cython, scipy, pytables, matplotlib, statsmodels, openpyxl

Background - IPython
--------------------

IPython is a fancy python console.  Try running ``ipython`` or ``ipython
--pylab`` on your command line.  Some IPython tips

.. code-block:: python

   # Special commands, 'magic functions', begin with %
   %quickref, %who, %run, %reset
   # Shell Commands
   ls, cd, pwd, mkdir
   help(), help(obj)
   # Tab completion of variables, attributes and methods

Background - IPython Notebook
-----------------------------

There is a web interface to IPython, known as the IPython notebook, start it
like this

.. code-block:: bash

    ipython notebook
    # or to get all of the pylab components
    ipython notebook --pylab


IPython - Follow Along
----------------------

Follow along by connecting to one of these servers.

* http://ipynb1.desertpy.com
* http://ipynb2.desertpy.com

NOTE: Only active on presentation day.

Background - NumPy
------------------

* NumPy is the foundation for Pandas
* Numerical data structures (mostly Arrays)
* Operations on those.
* Less structure than Pandas provides.

Background - NumPy - Arrays
---------------------------

.. code-block:: python

    import numpy as np
    # np.zeros, np.ones
    data0 = np.zeros((2, 4))
    #array([[ 0.,  0.,  0.,  0.],
    #       [ 0.,  0.,  0.,  0.]])
    data1 = np.arange(100)
    #array([  0, 1, 2, .. 99])

Background - NumPy - Arrays
---------------------------
.. code-block:: python

    data = np.arange(20).reshape(4, 5)
    #array([[ 0,  1,  2,  3,  4],
    #       [ 5,  6,  7,  8,  9],
    #       [10, 11, 12, 13, 14],
    #       [15, 16, 17, 18, 19]])
    data.dtype    #dtype('int64')
    result = data * 20.5
    #array([[ 0. , 20.5, 41. , 61.5, 82. ], ...
    #dtype('float64')

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

        Pandas and Friends

.. footer::

        © Austin Godber (@godber), 2013
