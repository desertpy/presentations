DesertPy Presentations
======================

Presentations for the DesertPy Group are shared in this repository and
can be found online on the
[DesertPy Presentation Website](http://desertpy.com/pages/presentations.html).

Creating a Presentation
-----------------------

If want to give a presentation you may use our format, which currently
uses [landslide](https://github.com/adamzap/landslide).  Landslide
supports presentations written in Markdown or Restructured Text and
generates a decent HTML5 style slideshow.  Support for other presentation
formats are just a little work and a pull request away ;)

* Fork
* make virtual env with requirements.txt
* stub out presentation directory with fab create
* write presentation
* TODO: build with `fab build` (only builds my presentation so far)
* commit and send pull request with your added presentation

Publish Presentations
---------------------

Members of DesertPy with publish capabilities can publish the main
presentation site.

* Checkout source
* make virtual env with requirements.txt
* TODO: build with `fab build` (only builds my presentation so far)
* publish to gh-pages branch with `fab publish`


