all: thesis.pdf

view: thesis.pdf
	open thesis.pdf

py:
	cat ../pysom/README |texifypython -l 70 > README.tex
	cat ../pysom/som.py |texifypython -l 70 > som_py.tex
	cat ../pysom/data.py |texifypython -l 70 > data_py.tex
	cat ../pysom/topology.py |texifypython -l 70 > topology_py.tex
	cat ../pysom/networkFunctions.py |texifypython -l 70 > networkFunctions_py.tex

thesis.pdf: ../bib/*.bib *.tex *.cls
	( pdflatex thesis || rm -f thesis.pdf ) && \
	bibtex thesis && \
	( pdflatex thesis || rm -f thesis.pdf ) && \
	( pdflatex thesis ) && \
	( pdflatex thesis ) && \
	echo "\n\n\n\n\n\n DOUBLE CHECK THIS LINE IN YOUR .toc: \contentsline {schapter}{BIBLIOGRAPHY}{39} \n\n\n\n\n\n" && \
	echo "\n\n\n\n\n\n"

clean:
	rm -f *.aux *.bbl *.blg *.dvi *.log *.lot *.toc *.lof thesis.ps thesis.pdf
