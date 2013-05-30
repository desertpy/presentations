A Presentation on Python's virtualenv.

For rst2pdf to correctly include the PNG file, it must be properly built with
PNG support.  I haven't worked out the dependencies for this in a virtualenv,
but the rst2pdf you get from apt-get in ubuntu works fine.

Build with::

  rst2pdf virtualenv.rst -b1 -s screen.json
