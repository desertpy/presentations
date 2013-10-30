all: presentation html

presentation: presentation.rst screen.json
	rst2pdf -b1 -s screen.json presentation.rst

html: presentation.rst
	landslide presentation.rst presentation.html

clean:
	rm presentation.pdf presentation.html
