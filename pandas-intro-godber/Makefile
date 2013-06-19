all: presentation html

presentation: presentation.rst screen.json
	rst2pdf -b1 -s screen.json presentation.rst

html: presentation.rst
	PYTHONPATH=~/Workspace/rst2html5/ ~/Workspace/rst2html5/bin/rst2html5 --deck-js --pretty-print-code --embed-content presentation.rst > presentation-deck.html
	PYTHONPATH=~/Workspace/rst2html5/ ~/Workspace/rst2html5/bin/rst2html5 --jquery --reveal-js --pretty-print-code --embed-content presentation.rst > presentation-reveal.html


clean:
	rm presentation.pdf presentation*.html
